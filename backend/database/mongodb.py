from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
        # Lazily cached collection handles
        self._col_datasets = None
        self._col_predictions = None
        self._col_historical = None
        self._col_metadata = None
    
    def connect(self):
        """Establish a client connection and prime common collections."""
        try:
            mongodb_uri = os.getenv('MONGOURI')
            if not mongodb_uri:
                raise ValueError("MONGOURI environment variable not set")
            
            self.client = MongoClient(mongodb_uri)
            self.db = self.client.fintech
            # Initialize common collections
            self._col_datasets = self.db.datasets
            self._col_predictions = self.db.predictions
            self._col_historical = self.db.historical_prices
            self._col_metadata = self.db.metadata
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB successfully")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
    
    def test_connection(self):
        """Ping the admin DB to verify connectivity."""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
        except:
            pass
        return False
    
    def save_dataset(self, dataset_data):
        """Insert a dataset document and return the insert result."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._col_datasets or self.db.datasets
            result = collection.insert_one(dataset_data)
            return result
        except Exception as e:
            print(f"Error saving dataset: {e}")
            raise
    
    def get_dataset_by_id(self, dataset_id):
        """Find a dataset by its ObjectId string."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._col_datasets or self.db.datasets
            from bson import ObjectId
            return collection.find_one({"_id": ObjectId(dataset_id)})
        except Exception as e:
            print(f"Error getting dataset: {e}")
            return None
    
    def get_all_datasets(self):
        """Return all dataset documents, newest first, with NaNs cleaned."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._col_datasets or self.db.datasets
            datasets = list(collection.find().sort("generated_at", -1))
            
            # Convert ObjectId to string and handle NaN values for JSON serialization
            for dataset in datasets:
                dataset['_id'] = str(dataset['_id'])
                # Clean up data array to handle NaN values
                if 'data' in dataset and isinstance(dataset['data'], list):
                    for record in dataset['data']:
                        self._clean_nan_values(record)
            
            return datasets
        except Exception as e:
            print(f"Error getting datasets: {e}")
            return []
    
    def _clean_nan_values(self, obj):
        """Recursively convert NaN values to None for JSON safety."""
        import math
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, float) and math.isnan(value):
                    obj[key] = None
                elif isinstance(value, dict):
                    self._clean_nan_values(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._clean_nan_values(item)
        return obj
    
    def get_recent_datasets(self, limit=10):
        """Summarize the most recent datasets for UI display."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._datasets_col or self.db.datasets
            datasets = list(collection.find().sort("generated_at", -1).limit(limit))
            
            # Convert ObjectId to string and format for frontend
            formatted_datasets = []
            for dataset in datasets:
                formatted_datasets.append({
                    'id': str(dataset['_id']),
                    'symbol': dataset.get('symbol', 'N/A'),
                    'date': dataset.get('generated_at', datetime.now()).strftime('%Y-%m-%d'),
                    'records': dataset.get('records', 0),
                    'exchange': dataset.get('exchange', 'N/A')
                })
            
            return formatted_datasets
        except Exception as e:
            print(f"Error getting recent datasets: {e}")
            return []
    
    def get_latest_data(self, symbol):
        """Return the latest dataset document for a given symbol."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._datasets_col or self.db.datasets
            latest = collection.find_one(
                {"symbol": symbol},
                sort=[("generated_at", -1)]
            )
            return latest
        except Exception as e:
            print(f"Error getting latest data: {e}")
            return None
    
    def save_prediction(self, prediction_data):
        """Insert a prediction record and return the insert result."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._col_predictions or self.db.predictions
            result = collection.insert_one(prediction_data)
            return result
        except Exception as e:
            print(f"Error saving prediction: {e}")
            raise
    
    def get_recent_predictions(self, limit=10):
        """Return the latest prediction documents, limited by count."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            collection = self._col_predictions or self.db.predictions
            predictions = list(collection.find().sort("created_at", -1).limit(limit))
            
            # Convert ObjectId to string
            for prediction in predictions:
                prediction['_id'] = str(prediction['_id'])
            
            return predictions
        except Exception as e:
            print(f"Error getting predictions: {e}")
            return []

    # New: Historical Prices APIs
    def save_historical_prices(self, symbol, exchange, prices):
        """Bulk-insert curated OHLCV rows into `historical_prices` for a symbol."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            collection = self._col_historical or self.db.historical_prices
            if not prices:
                print("⚠️ No prices data provided to save_historical_prices")
                return None
            
            print(f"💾 Saving {len(prices)} historical price records for {symbol}")
            
            # First, remove existing records for this symbol to avoid duplicates
            collection.delete_many({'symbol': symbol, 'exchange': exchange})
            
            docs = []
            for i, p in enumerate(prices):
                try:
                    doc = {
                        'symbol': symbol,
                        'exchange': exchange,
                        'date': p.get('date'),
                        'open': float(p.get('open_price') or p.get('open') or 0),
                        'high': float(p.get('high_price') or p.get('high') or 0),
                        'low': float(p.get('low_price') or p.get('low') or 0),
                        'close': float(p.get('close_price') or p.get('close') or 0),
                        'volume': int(p.get('volume') or 0)
                    }
                    docs.append(doc)
                except Exception as e:
                    print(f"⚠️ Error processing price record {i}: {e}")
                    continue
            
            if docs:
                result = collection.insert_many(docs, ordered=False)
                print(f"✅ Successfully saved {len(result.inserted_ids)} historical price records")
                return result
            else:
                print("❌ No valid price records to save")
                return None
        except Exception as e:
            print(f"❌ Error saving historical prices: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_prices(self, symbol, start_date=None, end_date=None, limit=500):
        """Query historical OHLCV rows filtered by symbol and optional date range."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            collection = self._col_historical or self.db.historical_prices
            query = {'symbol': symbol}
            if start_date or end_date:
                query['date'] = {}
                if start_date:
                    query['date']['$gte'] = start_date
                if end_date:
                    query['date']['$lte'] = end_date
            cursor = collection.find(query).sort('date', 1).limit(int(limit) if limit else 0)
            rows = []
            for doc in cursor:
                rows.append({
                    'symbol': doc.get('symbol'),
                    'date': doc.get('date'),
                    'open': float(doc.get('open', 0)),
                    'high': float(doc.get('high', 0)),
                    'low': float(doc.get('low', 0)),
                    'close': float(doc.get('close', 0)),
                    'volume': int(doc.get('volume', 0))
                })
            return rows
        except Exception as e:
            print(f"Error getting prices: {e}")
            return []

    # New: Forecast and Metadata helpers
    def save_forecast(self, forecast_data):
        """Insert a forecast document with model metadata and predictions."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            collection = self._col_predictions or self.db.predictions
            result = collection.insert_one(forecast_data)
            return result
        except Exception as e:
            print(f"Error saving forecast: {e}")
            raise

    def get_predictions(self, symbol=None, horizon=None, model=None, limit=50):
        """Query predictions by optional symbol, horizon, and model filters."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            collection = self._predictions_col or self.db.predictions
            query = {}
            if symbol:
                query['symbol'] = symbol
            if horizon:
                query['forecast_horizon'] = horizon
            if model:
                query['model'] = model
            print(f"🔍 Querying predictions with filters: {query}")
            cursor = collection.find(query).sort('created_at', -1).limit(int(limit) if limit else 0)
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                results.append(doc)
            print(f"📊 Found {len(results)} predictions matching query")
            return results
        except Exception as e:
            print(f"Error getting predictions: {e}")
            return []

    def upsert_metadata(self, symbol, metadata):
        """Create or update a symbol's metadata (info, sources, logs)."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            
            print(f"💾 Upserting metadata for symbol: {symbol}")
            collection = self._col_metadata or self.db.metadata
            from pymongo import ReturnDocument
            
            update_doc = {
                '$set': {
                    'symbol': symbol,
                    'instrument_info': metadata.get('instrument_info'),
                    'data_sources': metadata.get('data_sources'),
                    'last_updated': datetime.now()
                },
                '$setOnInsert': {'created_at': datetime.now()}
            }
            
            # Add update logs if provided
            if metadata.get('update_logs'):
                update_doc['$push'] = {'update_logs': {'$each': metadata.get('update_logs', [])}}
            
            updated = collection.find_one_and_update(
                {'symbol': symbol},
                update_doc,
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            
            if updated and '_id' in updated:
                updated['_id'] = str(updated['_id'])
            
            print(f"✅ Successfully upserted metadata for {symbol}")
            return updated
        except Exception as e:
            print(f"❌ Error upserting metadata for {symbol}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_metadata(self, symbol=None):
        """Fetch metadata for one symbol or return a list for all."""
        try:
            if self.db is None:
                raise Exception("Database not connected")
            collection = self._col_metadata or self.db.metadata
            if symbol:
                doc = collection.find_one({'symbol': symbol})
                if doc and '_id' in doc:
                    doc['_id'] = str(doc['_id'])
                return doc
            docs = list(collection.find())
            for d in docs:
                d['_id'] = str(d['_id'])
            return docs
        except Exception as e:
            print(f"Error getting metadata: {e}")
            return None if symbol else []
    
    def count_datasets(self):
        """Count dataset documents available in the collection."""
        try:
            if self.db is None:
                return 0
            
            collection = self._col_datasets or self.db.datasets
            return collection.count_documents({})
        except:
            return 0
    
    def count_records(self):
        """Aggregate the total curated records across datasets."""
        try:
            if self.db is None:
                return 0
            
            collection = self._col_datasets or self.db.datasets
            pipeline = [{"$group": {"_id": None, "total": {"$sum": "$records"}}}]
            result = list(collection.aggregate(pipeline))
            return result[0]['total'] if result else 0
        except:
            return 0
    
    def get_last_generated_date(self):
        """Return the latest dataset generation timestamp as a string."""
        try:
            if self.db is None:
                return None
            
            collection = self._datasets_col or self.db.datasets
            latest = collection.find_one(sort=[("generated_at", -1)])
            return latest['generated_at'].strftime('%Y-%m-%d %H:%M:%S') if latest else None
        except:
            return None
    
    def close(self):
        """Close the underlying client connection."""
        if self.client:
            self.client.close()