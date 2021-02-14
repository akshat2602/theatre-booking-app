from rest_framework.test import APITestCase
from django.urls import reverse
import uuid


class OccupySeatTestCase(APITestCase):
    url = reverse("occupy_seat")

    def test_seat_occupy(self):
        """
        Test to verify that seat booking works
        """
        data = {
            "name": "Akshat",
            "ticket": uuid.uuid4()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_uuid_already_exists(self):
        """
        Test to verify that duplicate ticket id is not allowed for booking
        """
        ticket_id = uuid.uuid4()
        data_1 = {
            "name": "Akshat",
            "ticket": ticket_id
        }
        response = self.client.post(self.url, data_1)
        self.assertEqual(201, response.status_code)

        data_2 = {
            "name": "Rugved",
            "ticket": ticket_id
        }
        response = self.client.post(self.url, data_2)
        self.assertEqual(409, response.status_code)


class VacateSeatTestCase(APITestCase):
    post_url = reverse("occupy_seat")
    delete_url = reverse("vacate_seat")

    def test_vacate_seat(self):
        """
        Test to verify vacate seat is working as intended
        """
        data_1 = {
            "name": "Akshat",
            "ticket": uuid.uuid4()
        }
        response = self.client.post(self.post_url, data_1)
        self.assertEqual(201, response.status_code)

        data_2 = {
            "name": "Rugved",
            "ticket": uuid.uuid4()
        }
        response = self.client.post(self.post_url, data_2)
        self.assertEqual(201, response.status_code)

        vacate_data = {
            "seat_number": response.data['seat_number']
        }
        response = self.client.delete(self.delete_url, vacate_data)
        self.assertEqual(204, response.status_code)

    def test_seat_number(self):
        """
        Test for if seat is already vacant
        """
        data = {
            "name": "Rugved",
            "ticket": uuid.uuid4()
        }
        response = self.client.post(self.post_url, data)
        self.assertEqual(201, response.status_code)

        vacate_data = {
            "seat_number": 10
        }
        response = self.client.delete(self.delete_url, vacate_data)
        self.assertEqual(404, response.status_code)


class test_get_info(APITestCase):
    post_url = reverse("occupy_seat")
    delete_url = reverse("vacate_seat")
    ticket = uuid.uuid4()

    def getInfo_url(self, pk):
        return reverse("get_info", kwargs={"pk": pk})

    def setUp(self):
        data = {
            "name": "Rugved",
            "ticket": self.ticket
        }
        self.client.post(self.post_url, data)

    def test_by_name(self):
        """
        Test to get info by name and return not found if name is not found
        """
        data = {
            "name": "Rugved"
        }
        response = self.client.get(self.getInfo_url(data['name']))
        self.assertEqual(302, response.status_code)

        data = {
            "name": "Rajat"
        }
        response = self.client.get(self.getInfo_url(data['name']))
        self.assertEqual(404, response.status_code)

    def test_by_uuid(self):
        """
        Test to get info by uuid and return not found if uuid is not found
        """
        data = {
            "ticket": self.ticket
        }
        response = self.client.get(self.getInfo_url(data['ticket']))
        self.assertEqual(302, response.status_code)

        data = {
            "ticket": uuid.uuid4()
        }
        response = self.client.get(self.getInfo_url(data['ticket']))
        self.assertEqual(404, response.status_code)

    def test_by_seat_number(self):
        """
        Test to get info by seat number and return not found if seat number is not found
        """
        data = {
            "seat_number": 1
        }
        response = self.client.get(self.getInfo_url(data['seat_number']))
        self.assertEqual(302, response.status_code)
        data = {
            "seat_number": 10
        }
        response = self.client.get(self.getInfo_url(data['seat_number']))
        print(response.data)
        self.assertEqual(404, response.status_code)
