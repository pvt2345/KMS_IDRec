Hướng dẫn chạy thử Graph Database từ python:

- Vào thư mục D:\Neo4j\neo4j-community-3.4.7\bin chạy lệnh cmd : "neo4j console" và đợi hiển thị đã remote thành công.
- Mở browser lên vào "localhost:7474" kiểm tra xem server đã chạy chưa.
- Chạy file D:\Neo4j\graph.py (phải cài package neo4j-driver trong python trước).
- Nếu chạy thành công, trên màn hình pycharm hiện ra thông báo các node đã được tạo ra.
- Vào browser truy vấn "MATCH (n:VanBan) RETURN n" sẽ thấy database được tạo.