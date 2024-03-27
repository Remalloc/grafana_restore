import json
import re
from datetime import datetime

import dataset
from pypinyin import lazy_pinyin, Style


def generate_slug(title):
    slug_title = ""
    for char in title:
        if re.match(r"[\u4e00-\u9fa5]", char):  # Check Chinese character
            slug_title += "".join(lazy_pinyin(char, style=Style.NORMAL)).lower() + "-"
        else:
            slug_title += char.lower()
    # remove all non-alphabet and non-number, replace " " to "-"
    slug = re.sub(r"[^a-z0-9\s-]", "", slug_title).replace(" ", "-")
    slug = slug.strip('-')
    if not slug or slug == '-':
        raise ValueError(f"Error slug: {slug}")
    return slug


class Restore(object):
    def __init__(self, db_url: str, org_id: int):
        self.db = dataset.connect(db_url)
        self.org_id = org_id
        self.folder_id = self.get_folder()

    def get_folder(self):
        uid = "XxzVe61In"
        rows = list(self.db["dashboard"].find(uid=uid))
        if rows:
            return rows[0]["id"]
        else:
            ids = list(self.db.query("SELECT max(dashboard_id) FROM dashboard_version"))
            if not ids:
                raise ValueError("Table dashboard_version is empty")
            max_id = ids[0]["dashboard_id"] + 1
            self.db["dashboard"].insert(
                {
                    "id": max_id,
                    "version": 0,
                    "slug": "Restore",
                    "title": "Restore",
                    "org_id": self.org_id,
                    "data": json.dumps({"schemaVersion": 17, "title": "Restore", "uid": uid, "version": 1}),
                    "created": datetime.now(),
                    "updated": datetime.now(),
                    "created_by": 1,
                    "updated_by": 1,
                    "gnet_id": 0,
                    "plugin_id": "",
                    "folder_id": 0,
                    "is_folder": 1,
                    "has_acl": 0,
                    "uid": uid
                }
            )
            return self.get_folder()

    def get_his_dashboard(self) -> dict:
        rows = self.db.query("""
            SELECT * FROM dashboard_version AS main
            WHERE main.version = ( SELECT MAX( version )
            FROM dashboard_version AS sub WHERE sub.dashboard_id = main.dashboard_id )
            ORDER BY created
            """)
        result = {}
        for row in rows:
            row["data"] = json.loads(row["data"])
            result[row["dashboard_id"]] = row
        return result

    def get_current_dashboard(self) -> dict:
        rows = self.db["dashboard"].find()
        result = {}
        for row in rows:
            row["data"] = json.loads(row["data"])
            result[row["id"]] = row
        return result

    def run(self):
        current_dashboards = self.get_current_dashboard()
        title_set = {x["data"]["title"] for x in current_dashboards.values()}
        his_dashboards = self.get_his_dashboard()
        for dashboard_id, value in his_dashboards.items():
            data = value["data"]
            title = data["title"]
            # rename conflict title
            if title in title_set:
                title += "-" + data["uid"]
            if dashboard_id in current_dashboards:
                print(f"Ignoring exist dashboard {title} {dashboard_id}")
            elif data.get("panels"):
                print(f"Adding dashboard {title} {dashboard_id}")
                slug = generate_slug(title)
                self.db["dashboard"].upsert(
                    {
                        "id": dashboard_id,
                        "version": data["version"],
                        "slug": slug,
                        "title": title,
                        "data": json.dumps(data),
                        "org_id": self.org_id,
                        "created": datetime.now(),
                        "updated": datetime.now(),
                        "created_by": 1,
                        "updated_by": 1,
                        "gnet_id": 0,
                        "plugin_id": "",
                        "folder_id": self.folder_id,
                        "is_folder": 0,
                        "has_acl": 0,
                        "uid": data["uid"]
                    },
                    ["uid"]
                )


def main():
    restore = Restore(db_url="sqlite:///grafana.db", org_id=8)
    restore.run()


if __name__ == "__main__":
    main()
