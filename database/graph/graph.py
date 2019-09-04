import json
import sys
from neo4j.v1 import GraphDatabase


class GraphDtb(object):

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j"):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=15)

    def close(self):
        self._driver.close()

    def make_node(self, name):
        with self._driver.session() as session:
            notification = session.write_transaction(self._create_and_return_vanban, name)
            print(notification)

    def make_relationship(self, _from, _to, _llk):
        with self._driver.session() as session:
            session.write_transaction(self._create_and_return_lienket, _from, _to, _llk)

    def delete_nodes(self):
        self.delete_relationships()
        with self._driver.session() as session:
            session.run("MATCH (n:VanBan) DELETE n")

    def delete_relationships(self):
        with self._driver.session() as session:
            session.run("MATCH ()-[n:LienKet]->() DELETE n")

    @staticmethod
    def _create_and_return_vanban(tx, name):
        result = tx.run("MERGE (vb:VanBan {svb: $name})"
                        "RETURN vb.svb + ' is created as node ' + id(vb)", name=name)
        # return result[0]["vb.svb"]
        return result.single()[0]

    def _create_and_return_lienket(cls, tx, _from, _to, _llk):
        tx.run("MATCH (from:VanBan {svb: $_from})"
               "MATCH (to:VanBan {svb: $_to})"
               "MERGE (from)-[lk:LienKet {llk: $_llk}]->(to)", _from=_from, _to=_to, _llk=_llk)


def main(path="Output_2.json"):  # path den file json
    data = json.loads(open(path, encoding='utf-8').read())
    dtb = GraphDtb(password='1234')
    dtb.delete_nodes()
    for item in data:
        svb = item["SVB"]
        vblk = item["VBLK"]
        llk = item["LLK"]
        dtb.make_node(svb)
        for vb in vblk:
            dtb.make_node(vb)
            dtb.make_relationship(svb, vb, llk)
    dtb.close()


if __name__ == "__main__":
    # main(sys.argv[0])
    # main()
    # from database.mysql_utils import DataAccess
    # dt = DataAccess().GetDataLienKet()
    # json.dump(dt,open('data_lien_ket.json','w',encoding='utf-8'),ensure_ascii=False)
    dt = json.load(open('data_lien_ket.json',encoding='utf-8'))
    dtb = GraphDtb(password='1234')
    dtb.delete_nodes()
    for record in dt:
        dtb.make_node(record['Số văn bản'])
        dtb.make_node(record['Văn bản liên kết'])
        dtb.make_relationship(record['Số văn bản'],record['Văn bản liên kết'],record['Loại liên kết'])