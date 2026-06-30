"""
================================================================
欺诈检测平台 — ETL 数据管道
功能: CSV/API数据获取 → 清洗 → 特征工程 → 分区存储
学生: 曾绍强  学号: 23110941038
================================================================
"""
import csv, json, time, os, hashlib, random
from collections import defaultdict

STU = "曾绍强 23110941038"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "processed_data")
os.makedirs(OUT_DIR, exist_ok=True)


class ETLPipeline:
    def __init__(self):
        self.stats = {}
        self.etl_log = []

    def log(self, msg):
        ts = time.strftime('%H:%M:%S')
        self.etl_log.append(f"[{ts}] {msg}")
        print(f"  [{ts}] {msg}")

    def extract_csv(self, csv_path, limit=None):
        """数据源1: CSV批量提取"""
        self.log(f"EXTRACT CSV: {os.path.basename(csv_path)}")
        data = []
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and i >= limit:
                    break
                data.append(row)
        self.stats['csv_raw'] = len(data)
        self.log(f"  提取 {len(data)} 行")
        return data

    def extract_api(self, n_records=500):
        """数据源2: API实时获取"""
        self.log(f"EXTRACT API: 模拟RESTful接口 ({n_records}条)")
        data = []
        for i in range(n_records):
            data.append({
                'Time': str(random.randint(0, 172800)),
                'V1': str(round(random.gauss(0, 1.5), 4)),
                'V2': str(round(random.gauss(0, 1.2), 4)),
                'Amount': str(round(random.lognormvariate(4.0, 1.0), 2)),
                'is_fraud': '1' if random.random() < 0.005 else '0',
                'source': 'api',
                'fetch_time': time.strftime('%Y-%m-%dT%H:%M:%S'),
            })
        self.stats['api_raw'] = len(data)
        self.log(f"  提取 {len(data)} 行")
        return data

    def clean(self, data):
        """数据清洗"""
        self.log(f"CLEAN: 开始清洗 {len(data)} 行")
        before = len(data)
        cleaned = []
        removed_amount = 0
        removed_null = 0

        for row in data:
            try:
                amount = float(row.get('Amount', 0))
                if amount <= 0:
                    removed_amount += 1
                    continue
                if row.get('V1') is None or row.get('V2') is None:
                    removed_null += 1
                    continue
                cleaned.append(row)
            except:
                removed_null += 1

        self.stats['clean_before'] = before
        self.stats['clean_after'] = len(cleaned)
        self.stats['clean_removed'] = before - len(cleaned)
        self.log(f"  清洗后 {len(cleaned)} 行 (删除 {before-len(cleaned)}: "
                 f"金额异常{removed_amount}, 空值{removed_null})")
        return cleaned

    def transform(self, data):
        """特征工程"""
        self.log(f"TRANSFORM: 特征工程")
        for row in data:
            t = float(row.get('Time', 0))
            row['hour_bin'] = str(int(t // 3600) % 24)
            row['is_night'] = '1' if int(row['hour_bin']) in range(0, 6) else '0'
            row['amount_log'] = str(round(float(row.get('Amount', 1)) ** 0.5, 2))
        self.stats['transformed'] = len(data)
        self.log(f"  新增特征: hour_bin, is_night, amount_log")
        return data

    def partition_store(self, data, partition_key='hour_bin', n_partitions=24):
        """分区存储"""
        self.log(f"PARTITION: 按 {partition_key} 分 {n_partitions} 区")
        partitions = defaultdict(list)
        for row in data:
            pk = row.get(partition_key, '0')
            partitions[pk].append(row)

        for pk in sorted(partitions.keys()):
            part_path = os.path.join(OUT_DIR, f"{partition_key}={pk}")
            os.makedirs(part_path, exist_ok=True)
            part_file = os.path.join(part_path, f"part-{pk}.json")
            with open(part_file, 'w') as f:
                json.dump(partitions[pk][:100], f)  # 每分区存前100条示例

        non_empty = len([p for p in partitions if partitions[p]])
        self.stats['partitions'] = non_empty
        self.log(f"  非空分区: {non_empty}/{n_partitions}, "
                 f"目录: {OUT_DIR}/{partition_key}=X/")
        return partitions

    def run(self, csv_path, api_records=500):
        """完整ETL流程"""
        print(f"\n{'='*55}")
        print(f"  ETL Pipeline — 反欺诈数据管道 | {STU}")
        print(f"{'='*55}")

        # Extract
        csv_data = self.extract_csv(csv_path, limit=20000)
        api_data = self.extract_api(api_records)
        all_data = csv_data + api_data

        # Transform
        all_data = self.clean(all_data)
        all_data = self.transform(all_data)

        # Load (分区存储)
        partitions = self.partition_store(all_data)

        # 统计
        print(f"\n[ETL完成]")
        print(f"  数据源: CSV({self.stats['csv_raw']}) + API({self.stats['api_raw']})")
        print(f"  清洗后: {self.stats['clean_after']} 行")
        print(f"  保留率: {self.stats['clean_after']/(self.stats['csv_raw']+self.stats['api_raw'])*100:.1f}%")
        print(f"  分区数: {self.stats['partitions']}")
        print(f"  输出目录: {OUT_DIR}")

        return all_data


if __name__ == "__main__":
    csv_path = os.path.join(BASE, "creditcard.csv")
    pipeline = ETLPipeline()
    pipeline.run(csv_path, api_records=500)
