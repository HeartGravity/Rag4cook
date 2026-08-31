import os
import random
from pymilvus import MilvusClient, DataType

def test_milvus_lite():
    print("=== 开始测试 Milvus Lite ===")
    
    # 1. 初始化客户端 (指定本地 .db 文件即自动启动 Milvus Lite)
    db_path = "./test_milvus_lite.db"
    if os.path.exists(db_path):
        os.remove(db_path) # 清理旧的测试数据
        
    client = MilvusClient(uri=db_path)
    print(f"✅ 成功连接到 Milvus Lite (文件: {db_path})")

    collection_name = "test_collection"
    dim = 128

    # 2. 创建集合
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        dimension=dim,
        metric_type="COSINE" 
    )
    print(f"✅ 成功创建集合: {collection_name}，维度: {dim}")

    # 3. 准备并插入模拟数据
    # 生成 5 条随机向量数据
    data = []
    for i in range(5):
        vector = [random.uniform(-1, 1) for _ in range(dim)]
        data.append({
            "id": i,
            "vector": vector,
            "text": f"这是测试文档块_{i}",
            "recipe_name": f"测试菜谱_{i}"
        })

    res = client.insert(collection_name=collection_name, data=data)
    print(f"✅ 成功插入 {res['insert_count']} 条数据")

    # 4. 执行相似度检索
    query_vector = [[random.uniform(-1, 1) for _ in range(dim)]]
    
    print("\n🔍 开始检索...")
    search_res = client.search(
        collection_name=collection_name,
        data=query_vector,
        limit=2,
        output_fields=["text", "recipe_name"]
    )

    # 5. 打印结果
    for hits in search_res:
        for hit in hits:
            print(f" - 找到匹配项: ID={hit['id']}, 距离/得分={hit['distance']:.4f}")
            print(f"   内容: {hit['entity']['text']}")
            
    print("\n🎉 Milvus Lite 测试全部通过！")

if __name__ == "__main__":
    test_milvus_lite()