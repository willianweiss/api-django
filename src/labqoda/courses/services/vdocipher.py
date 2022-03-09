import requests
from django.conf import settings
from requests_toolbelt import MultipartEncoder


class VdoCipher:

    BASE_URL = settings.VDOCHIPER_BASE_URL
    API_KEY = settings.VDOCHIPER_API_KEY

    @property
    def headers(self):
        return {"Authorization": "Apisecret " + self.API_KEY}

    def make_credentials(self, title):
        querystring = {"title": title}
        response = requests.request(
            "PUT", self.BASE_URL, headers=self.headers, params=querystring
        )

        if response.status_code > 300:
            raise Exception("Permission error on VdoChiper API")

        return response.json()

    def upload_file(self, credentials, file):
        clientPayload = credentials["clientPayload"]
        uploadLink = clientPayload["uploadLink"]
        m_data = MultipartEncoder(
            fields=[
                ("x-amz-credential", clientPayload["x-amz-credential"]),
                ("x-amz-algorithm", clientPayload["x-amz-algorithm"]),
                ("x-amz-date", clientPayload["x-amz-date"]),
                ("x-amz-signature", clientPayload["x-amz-signature"]),
                ("key", clientPayload["key"]),
                ("policy", clientPayload["policy"]),
                ("success_action_status", "201"),
                ("success_action_redirect", ""),
                ("file", file.read()),
            ]
        )

        response = requests.post(
            uploadLink,
            data=m_data,
            headers={"Content-Type": m_data.content_type},
        )

        response.raise_for_status()
        return response

    def get_video_render(self, video_id):
        url = self.BASE_URL + video_id + "/otp"
        body = {"ttl": 1000}

        response = requests.post(url, json=body, headers=self.headers)
        return response.json()

    def delete(self, video_id):
        url = self.BASE_URL
        querystring = {"videos": str(video_id)}
        response = requests.request(
            "DELETE", url, headers=self.headers, params=querystring
        )

        return response
