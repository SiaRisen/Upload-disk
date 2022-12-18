import requests
import os


TOKEN = " "


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {"Content-Type": "application/json",
                "Authorization": f"OAuth {self.token}"}

    def _get_folder_(self, path_folder):
        url_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        folder = requests.put(f"{url_folder}?path={path_folder}", headers=headers)

    def upload_file_to_disk(self, disk_path: str, file_path: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        disk_file_path = f"{disk_path}/{os.path.split(file_path)[1]}"
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        result = response.json()

        href = result.get("href", "")

        response = requests.put(href, data=open(file_path, "rb"))
        response.raise_for_status()
        if response.status_code == 201:
            print("Загрузка файла завершена")


if __name__ == "__main__":
    path_to_file = input("Введите путь загружаемого файла: ")
    path_to_folder = input("Введите имя папки на Yandex диске: ")
    token = input("Введите TOKEN: ")
    uploader = YaUploader(token)
    uploader._get_folder_(path_to_folder)
    uploader.upload_file_to_disk(path_to_folder, path_to_file)
