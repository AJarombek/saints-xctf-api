"""
Test suite for the API routes for groups of users (api/src/route/groupRoute.py)
Author: Andrew Jarombek
Date: 11/10/2019
"""

import json
from datetime import datetime

import asyncio
from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import (
    test_route_auth,
    AuthVariant,
    create_test_user,
    destroy_test_user,
    get_jwt_token,
)


class TestGroupRoute(TestSuite):
    def test_group_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups' route. This route is redirected to
        '/v2/groups/' by default.
        """
        response: Response = self.client.get(
            "/v2/groups", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn("/v2/groups/", headers.get("Location"))

    def test_group_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups' route.
        """
        test_route_auth(self, self.client, "GET", "/v2/groups", AuthVariant.FORBIDDEN)

    def test_group_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups", AuthVariant.UNAUTHORIZED
        )

    def test_group_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/' route.  This test proves that the endpoint returns
        a list of groups.
        """
        response: Response = self.client.get(
            "/v2/groups/", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups")
        self.assertGreater(len(response_json.get("groups")), 1)

    def test_group_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/' route.
        """
        test_route_auth(self, self.client, "GET", "/v2/groups/", AuthVariant.FORBIDDEN)

    def test_group_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/", AuthVariant.UNAUTHORIZED
        )

    def test_group_by_group_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        trying to retrieve a group with a name that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/invalid_group_name",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"), "/v2/groups/saintsxctf/invalid_group_name"
        )
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(response_json.get("error"), "there is no group with this name")

    def test_group_by_group_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        retrieving a group with a valid name results in the group and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/saintsxctf/wmenstf")
        self.assertIsNotNone(response_json.get("group"))

    def test_group_by_group_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/saintsxctf/wmenstf",
            AuthVariant.FORBIDDEN,
        )

    def test_group_by_group_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/saintsxctf/wmenstf",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_by_group_name_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        trying to update a group that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put(
            "/v2/groups/saintsxctf/invalid_group_name",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"), "/v2/groups/saintsxctf/invalid_group_name"
        )
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"), "there is no existing group with this name"
        )

    def test_group_by_group_name_put_route_400_not_an_admin(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        if the user trying to update a group is not an admin of that group group, a 400 error is returned.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))

        request_body = json.dumps(response_json.get("group"))

        response: Response = self.client.put(
            "/v2/groups/saintsxctf/wmenstf",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/saintsxctf/wmenstf")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to update a group with name wmenstf in team saintsxctf.",
        )

    def test_group_by_group_name_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        if the updated group is the same as the original group, a 400 error is returned.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/alumni",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))

        request_body = json.dumps(response_json.get("group"))

        response: Response = self.client.put(
            "/v2/groups/saintsxctf/alumni",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/saintsxctf/alumni")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"),
            "the group submitted is equal to the existing group with the same name",
        )

    def test_group_by_group_name_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.  This test proves that
        if a valid group JSON is passed to this endpoint, the existing group will be updated and a valid 200 response
        code will be returned.
        """
        request_body = json.dumps(
            {
                "group_name": "alumni",
                "group_title": "Alumni",
                "grouppic": "picture_bytes",
                "grouppic_name": "picture.png",
                "week_start": "sunday",
                "description": f"Updated: {datetime.now()}",
                "deleted": False,
            }
        )

        response: Response = self.client.put(
            "/v2/groups/saintsxctf/alumni",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/saintsxctf/alumni")
        self.assertTrue(response_json.get("updated"))
        self.assertIsNotNone(response_json.get("group"))

    def test_group_by_group_name_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "PUT",
            "/v2/groups/saintsxctf/alumni",
            AuthVariant.FORBIDDEN,
        )

    def test_group_by_group_name_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/groups/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "PUT",
            "/v2/groups/saintsxctf/alumni",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<group_id>' route.  This test proves that
        trying to retrieve a group with an id that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/0")
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(response_json.get("error"), "there is no group with this id")

    def test_group_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/<group_id>' route.  This test proves that
        retrieving a group with a valid id results in the group and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/1")
        self.assertIsNotNone(response_json.get("group"))

    def test_group_by_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/<group_id>' route.
        """
        test_route_auth(self, self.client, "GET", "/v2/groups/1", AuthVariant.FORBIDDEN)

    def test_group_by_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/1", AuthVariant.UNAUTHORIZED
        )

    def test_group_by_id_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_id>' route.  This test proves that
        trying to update a group that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put(
            "/v2/groups/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/0")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to update a group with id 0.",
        )

    def test_group_by_id_put_route_400_not_an_admin(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_id>' route.  This test proves that
        a user trying to update a group they are not an administrator of results in a 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        response: Response = self.client.put(
            f"/v2/groups/{group_id}", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), f"/v2/groups/{group_id}")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"),
            f"User andy is not authorized to update a group with id {group_id}.",
        )

    def test_group_by_id_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_id>' route.  This test proves that if the updated
        group is the same as the original group, a 400 error is returned.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/alumni",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        request_body = json.dumps(response_json.get("group"))

        response: Response = self.client.put(
            f"/v2/groups/{group_id}",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), f"/v2/groups/{group_id}")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group"))
        self.assertEqual(
            response_json.get("error"),
            "The group submitted is equal to the existing group with the same id.",
        )

    def test_group_by_id_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/<group_id>' route.  This test proves that if the updated
        group object is valid and the user is an admin of the group, the group is updated and a 200 status code is
        returned.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/alumni",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        group_dict: dict = response_json.get("group")
        group_dict["description"] = f"Updated: {datetime.now()}"
        request_body = json.dumps(group_dict)

        response: Response = self.client.put(
            f"/v2/groups/{group_id}",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), f"/v2/groups/{group_id}")
        self.assertTrue(response_json.get("updated"))
        self.assertIsNotNone(response_json.get("group"))

    def test_group_by_id_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/groups/<group_id>' route.
        """
        test_route_auth(self, self.client, "PUT", "/v2/groups/1", AuthVariant.FORBIDDEN)

    def test_group_by_id_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/groups/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "PUT", "/v2/groups/1", AuthVariant.UNAUTHORIZED
        )

    def test_team_by_group_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/team/<group_id>' route.  This test proves that
        trying to retrieve a team via a group id that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/team/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/team/0")
        self.assertIsNone(response_json.get("team"))
        self.assertEqual(
            response_json.get("error"), "No team exists that has a group with this id."
        )

    def test_team_by_group_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/team/<group_id>' route.  This test proves that
        retrieving a team via a valid group id results in the team and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/team/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/team/1")
        self.assertIsNotNone(response_json.get("team"))

    def test_team_by_group_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/team/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/team/1", AuthVariant.FORBIDDEN
        )

    def test_team_by_group_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/team/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/team/1", AuthVariant.UNAUTHORIZED
        )

    def test_group_members_by_group_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<team_name>/<group_name>' route.  This test
        proves that trying to retrieve group members from a group with a group name that doesn't exist results in a HTTP
        400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/members/saintsxctf/invalid_group_name",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"),
            "/v2/groups/members/saintsxctf/invalid_group_name",
        )
        self.assertEqual(
            response_json.get("group"), "/v2/groups/saintsxctf/invalid_group_name"
        )
        self.assertIsNone(response_json.get("group_members"))
        self.assertEqual(
            response_json.get("error"),
            "the group does not exist or there are no members in the group",
        )

    def test_group_members_by_group_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<team_name>/<group_name>' route.  This test
        proves that retrieving group members from a group with a valid group name results in the members and a 200
        status.
        """
        response: Response = self.client.get(
            "/v2/groups/members/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json.get("self"), "/v2/groups/members/saintsxctf/wmenstf"
        )
        self.assertEqual(response_json.get("group"), "/v2/groups/saintsxctf/wmenstf")
        self.assertIsNotNone(response_json.get("group_members"))
        self.assertGreaterEqual(len(response_json.get("group_members")), 1)
        self.assertIn("username", response_json.get("group_members")[0])
        self.assertIn("first", response_json.get("group_members")[0])
        self.assertIn("last", response_json.get("group_members")[0])
        self.assertIn("member_since", response_json.get("group_members")[0])
        self.assertIn("user", response_json.get("group_members")[0])
        self.assertNotIn("deleted", response_json.get("group_members")[0])
        self.assertIsNotNone(response_json.get("group_members")[0]["username"])

    def test_group_members_by_group_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/members/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/members/saintsxctf/wmenstf",
            AuthVariant.FORBIDDEN,
        )

    def test_group_members_by_group_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/members/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/members/saintsxctf/wmenstf",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_members_by_group_id_and_username_put_route_400_not_an_admin(
        self,
    ) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/members/<group_id>/<username>' route.  This test proves that
        the request results in an HTTP 400 error response if the user making the request is not an admin of the
        specified group.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/menstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        request_body = json.dumps({"status": "accepted", "user": "user"})
        response: Response = self.client.put(
            f"/v2/groups/members/{group_id}/andy",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"), f"/v2/groups/members/{group_id}/andy"
        )
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("group_member"))
        self.assertEqual(
            response_json.get("error"),
            f"User andy is not authorized to update the group membership for user andy in group with id {group_id}.",
        )

    def test_group_members_by_group_id_and_username_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/groups/members/<group_id>/<username>' route.  This test proves
        that the request results in an HTTP 200 response.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/alumni",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        # You know I'm always here for you no matter what.  Will always give you my best if you ask for it.
        request_body = json.dumps({"status": "accepted", "user": "admin"})
        response: Response = self.client.put(
            f"/v2/groups/members/{group_id}/andy",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json.get("self"), f"/v2/groups/members/{group_id}/andy"
        )
        self.assertTrue(response_json.get("updated"))
        self.assertIsNotNone(response_json.get("group_member"))

        group_member: dict = response_json.get("group_member")

        self.assertEqual(1, group_member.get("group_id"))
        self.assertEqual("alumni", group_member.get("group_name"))
        self.assertEqual("accepted", group_member.get("status"))
        self.assertEqual("admin", group_member.get("user"))
        self.assertEqual("andy", group_member.get("username"))

    def test_group_members_by_group_id_and_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/groups/members/<group_id>/<username>' route.
        """
        test_route_auth(
            self, self.client, "PUT", "/v2/groups/members/1/andy", AuthVariant.FORBIDDEN
        )

    def test_group_members_by_group_id_and_username_put_route_unauthorized(
        self,
    ) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/groups/members/<group_id>/<username>' route.
        """
        test_route_auth(
            self,
            self.client,
            "PUT",
            "/v2/groups/members/1/andy",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_members_by_group_id_and_username_delete_route_400_not_an_admin(
        self,
    ) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/groups/<group_id>/<username>' route.  This test proves
        that the request results in an HTTP 400 response if the user making the request is not an admin of the group.
        """
        response: Response = self.client.get(
            "/v2/groups/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        response: Response = self.client.delete(
            f"/v2/groups/members/{group_id}/andy",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"), f"/v2/groups/members/{group_id}/andy"
        )
        self.assertFalse(response_json.get("deleted"))
        self.assertEqual(
            response_json.get("error"),
            f"User andy is not authorized to delete the group membership for user andy in group with id {group_id}.",
        )

    def test_group_members_by_group_id_and_username_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/groups/members/<group_id>/<username>' route.  This test
        proves that the request results in an HTTP 204 response.
        """
        temporary_username: str = create_test_user(self)

        asyncio.run(
            get_jwt_token(
                test_suite=self,
                auth_url=self.auth_url,
                client_id=temporary_username,
                client_secret="password",
            )
        )

        request_body = json.dumps(
            {
                "teams_joined": ["saintsxctf"],
                "teams_left": [],
                "groups_joined": [{"team_name": "saintsxctf", "group_name": "alumni"}],
                "groups_left": [],
            }
        )

        response: Response = self.client.put(
            f"/v2/users/memberships/{temporary_username}",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwts.get(temporary_username)}"},
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json.get("self"), f"/v2/users/memberships/{temporary_username}"
        )
        self.assertTrue(response_json.get("updated"))

        response: Response = self.client.get(
            "/v2/groups/saintsxctf/alumni",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("group"))
        group_id = response_json.get("group").get("id")

        response: Response = self.client.delete(
            f"/v2/groups/members/{group_id}/{temporary_username}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        self.assertEqual(response.status_code, 204)

        destroy_test_user(self, temporary_username)

    def test_group_members_by_group_id_and_username_delete_route_forbidden(
        self,
    ) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/groups/members/<group_id>/<username>' route.
        """
        test_route_auth(
            self,
            self.client,
            "DELETE",
            "/v2/groups/members/1/andy",
            AuthVariant.FORBIDDEN,
        )

    def test_group_members_by_group_id_and_username_delete_route_unauthorized(
        self,
    ) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/groups/members/<group_id>/<username>' route.
        """
        test_route_auth(
            self,
            self.client,
            "DELETE",
            "/v2/groups/members/1/andy",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_members_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<group_id>' route.  This test
        proves that trying to retrieve group members from a group with an id that doesn't exist results in a HTTP
        400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/members/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/members/0")
        self.assertEqual(response_json.get("group"), "/v2/groups/0")
        self.assertIsNone(response_json.get("group_members"))
        self.assertEqual(
            response_json.get("error"),
            "a group does not exist with this id or the group has no members",
        )

    def test_group_members_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/members/<group_id>' route.  This test
        proves that retrieving group members from a group with a valid id results in the members and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/members/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/members/1")
        self.assertEqual(response_json.get("group"), "/v2/groups/1")
        self.assertIsNotNone(response_json.get("group_members"))
        self.assertGreaterEqual(len(response_json.get("group_members")), 1)
        self.assertIn("username", response_json.get("group_members")[0])
        self.assertIn("first", response_json.get("group_members")[0])
        self.assertIn("last", response_json.get("group_members")[0])
        self.assertIn("member_since", response_json.get("group_members")[0])
        self.assertIn("user", response_json.get("group_members")[0])
        self.assertNotIn("deleted", response_json.get("group_members")[0])
        self.assertIsNotNone(response_json.get("group_members")[0]["username"])

    def test_group_members_by_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/members/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/members/1", AuthVariant.FORBIDDEN
        )

    def test_group_members_by_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/members/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/members/1", AuthVariant.UNAUTHORIZED
        )

    def test_group_statistics_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/statistics/<group_id>' route.  This test
        proves that trying to retrieve group statistics from a group with an id that doesn't exist results in an HTTP
        400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/statistics/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/statistics/0")
        self.assertIsNone(response_json.get("stats"))
        self.assertEqual(response_json.get("error"), "there is no group with this id")

    def test_group_statistics_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/statistics/<group_id>' route.  This test
        proves that retrieving group statistics from a group with a valid id results in the stats and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/statistics/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/statistics/1")
        self.assertIsNotNone(response_json.get("stats"))

        statistics = response_json.get("stats")
        self.assertIn("miles_all_time", statistics)
        self.assertTrue(
            statistics.get("miles_all_time") is None
            or isinstance(statistics.get("miles_all_time"), float)
        )
        self.assertIn("miles_past_month", statistics)
        self.assertTrue(
            statistics.get("miles_past_month") is None
            or isinstance(statistics.get("miles_past_month"), float)
        )
        self.assertIn("miles_past_week", statistics)
        self.assertTrue(
            statistics.get("miles_past_week") is None
            or isinstance(statistics.get("miles_past_week"), float)
        )
        self.assertIn("miles_past_year", statistics)
        self.assertTrue(
            statistics.get("miles_past_year") is None
            or isinstance(statistics.get("miles_past_year"), float)
        )
        self.assertIn("run_miles_all_time", statistics)
        self.assertTrue(
            statistics.get("run_miles_all_time") is None
            or isinstance(statistics.get("run_miles_all_time"), float)
        )
        self.assertIn("run_miles_past_year", statistics)
        self.assertTrue(
            statistics.get("run_miles_past_year") is None
            or isinstance(statistics.get("run_miles_past_year"), float)
        )
        self.assertIn("run_miles_past_month", statistics)
        self.assertTrue(
            statistics.get("run_miles_past_month") is None
            or isinstance(statistics.get("run_miles_past_month"), float)
        )
        self.assertIn("run_miles_past_week", statistics)
        self.assertTrue(
            statistics.get("run_miles_past_week") is None
            or isinstance(statistics.get("run_miles_past_week"), float)
        )
        self.assertIn("feel_all_time", statistics)
        self.assertTrue(
            statistics.get("feel_all_time") is None
            or isinstance(statistics.get("feel_all_time"), float)
        )
        self.assertIn("feel_past_year", statistics)
        self.assertTrue(
            statistics.get("feel_past_year") is None
            or isinstance(statistics.get("feel_past_year"), float)
        )
        self.assertIn("feel_past_month", statistics)
        self.assertTrue(
            statistics.get("feel_past_month") is None
            or isinstance(statistics.get("feel_past_month"), float)
        )
        self.assertIn("feel_past_week", statistics)
        self.assertTrue(
            statistics.get("feel_past_week") is None
            or isinstance(statistics.get("feel_past_week"), float)
        )

    def test_group_statistics_by_id_get_route_200_expected_values(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/statistics/<group_id>' route.  This test
        proves that retrieving group statistics from a group with a valid id returns the expected data.
        """
        response: Response = self.client.get(
            "/v2/groups/statistics/7", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/statistics/7")
        self.assertIsNotNone(response_json.get("stats"))

        statistics = response_json.get("stats")
        self.assertEqual(25, statistics.get("miles_all_time"))
        self.assertEqual(7, statistics.get("miles_past_week"))

        self.assertEqual(3, statistics.get("run_miles_all_time"))
        self.assertEqual(2, statistics.get("run_miles_past_week"))

        self.assertEqual(8.7931, statistics.get("feel_all_time"))
        self.assertEqual(8.1429, statistics.get("feel_past_week"))

    def test_group_statistics_by_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/statistics/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/statistics/1", AuthVariant.FORBIDDEN
        )

    def test_group_statistics_by_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/statistics/<group_id>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/statistics/1",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_leaderboard_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard/<group_id>' route.  This test
        proves that trying to retrieve leaderboard information from a group with an id that doesn't exist results in an
        HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/leaderboard/0")
        self.assertIsNone(response_json.get("leaderboard"))
        self.assertEqual(response_json.get("error"), "there is no group with this id")

    def test_group_leaderboard_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard/<group_id>' route.  This test
        proves that trying to retrieve leaderboard information from a valid group results in leaderboard items and an
        HTTP 200 response code.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/leaderboard/1")
        self.assertIsNotNone(response_json.get("leaderboard"))

        leaderboard_items = response_json.get("leaderboard")
        self.assertGreater(len(leaderboard_items), 0)

        leaderboard_item = leaderboard_items[0]
        self.assertIn("username", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("username"), str))
        self.assertIn("first", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("first"), str))
        self.assertIn("last", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("last"), str))
        self.assertIn("miles", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("miles"), float))
        self.assertIn("miles_run", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("miles_run"), float))
        self.assertIn("miles_biked", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("miles_biked"), float))
        self.assertIn("miles_swam", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("miles_swam"), float))
        self.assertIn("miles_other", leaderboard_item)
        self.assertTrue(isinstance(leaderboard_item.get("miles_other"), float))

    def test_group_leaderboard_get_route_expected_values(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard' route.  This test
        proves that leaderboard information from a valid group has proper values.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/7",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)

        leaderboard_items = response_json.get("leaderboard")
        self.assertGreater(len(leaderboard_items), 0)

        leaderboard_item = leaderboard_items[0]
        self.assertEqual("dotty", leaderboard_item.get("username"))
        self.assertEqual("Dotty", leaderboard_item.get("first"))
        self.assertEqual("J", leaderboard_item.get("last"))
        self.assertEqual(23, leaderboard_item.get("miles"))
        self.assertEqual(2, leaderboard_item.get("miles_run"))
        self.assertEqual(2, leaderboard_item.get("miles_biked"))
        self.assertEqual(2, leaderboard_item.get("miles_swam"))
        self.assertEqual(17, leaderboard_item.get("miles_other"))

    def test_group_leaderboard_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/leaderboard/<group_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/groups/leaderboard/1", AuthVariant.FORBIDDEN
        )

    def test_group_leaderboard_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/leaderboard/<group_id>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/leaderboard/1",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_leaderboard_with_interval_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard/<group_id>/<interval>' route.  This test
        proves that trying to retrieve leaderboard information from a group with an id that doesn't exist results in an
        HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/0/week",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/groups/leaderboard/0/week")
        self.assertIsNone(response_json.get("leaderboard"))
        self.assertEqual(response_json.get("error"), "there is no group with this id")

    def test_group_leaderboard_with_interval_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard/<group_id>' route.  This test
        proves that trying to retrieve leaderboard information during an interval from a valid group results in
        leaderboard items and an HTTP 200 response code.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/1/year",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/leaderboard/1/year")
        self.assertIsNotNone(response_json.get("leaderboard"))

        leaderboard_items = response_json.get("leaderboard")

        if len(leaderboard_items) > 0:
            leaderboard_item = leaderboard_items[0]
            self.assertIn("username", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("username"), str))
            self.assertIn("first", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("first"), str))
            self.assertIn("last", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("last"), str))
            self.assertIn("miles", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("miles"), float))
            self.assertIn("miles_run", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("miles_run"), float))
            self.assertIn("miles_biked", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("miles_biked"), float))
            self.assertIn("miles_swam", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("miles_swam"), float))
            self.assertIn("miles_other", leaderboard_item)
            self.assertTrue(isinstance(leaderboard_item.get("miles_other"), float))
        else:
            self.assertEqual(
                "No leaderboard data was found within this group and time interval.",
                response_json.get("warning"),
            )

    def test_group_leaderboard_with_interval_get_route_expected_values(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/leaderboard/<group_id>/<interval>' route.  This test
        proves that leaderboard information in an interval from a valid group has proper values.
        """
        response: Response = self.client.get(
            "/v2/groups/leaderboard/7/week",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)

        leaderboard_items = response_json.get("leaderboard")
        self.assertGreater(len(leaderboard_items), 0)

        leaderboard_item = leaderboard_items[0]
        self.assertEqual("dotty", leaderboard_item.get("username"))
        self.assertEqual("Dotty", leaderboard_item.get("first"))
        self.assertEqual("J", leaderboard_item.get("last"))
        self.assertEqual(5, leaderboard_item.get("miles"))
        self.assertEqual(1, leaderboard_item.get("miles_run"))
        self.assertEqual(1, leaderboard_item.get("miles_biked"))
        self.assertEqual(1, leaderboard_item.get("miles_swam"))
        self.assertEqual(2, leaderboard_item.get("miles_other"))

    def test_group_leaderboard_with_interval_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/leaderboard/<group_id>/<interval>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/leaderboard/1/month",
            AuthVariant.FORBIDDEN,
        )

    def test_group_leaderboard_with_interval_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/leaderboard/<group_id>/<interval>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/leaderboard/1/month",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_snapshot_by_group_name_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/snapshot/<team_name>/<group_name>' route.  This test
        proves that trying to retrieve a snapshot about a group with a group name that doesn't exist results in a HTTP
        400 error.
        """
        response: Response = self.client.get(
            "/v2/groups/snapshot/saintsxctf/invalid_group_name",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"),
            "/v2/groups/snapshot/saintsxctf/invalid_group_name",
        )
        self.assertEqual(
            response_json.get("group"), "/v2/groups/saintsxctf/invalid_group_name"
        )
        self.assertIsNone(response_json.get("group_snapshot"))
        self.assertEqual(response_json.get("error"), "the group does not exist")

    def test_group_snapshot_by_group_name_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/snapshot/<team_name>/<group_name>' route.  This test
        proves that retrieving a snapshot about a group with a valid group name results in the group and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/groups/snapshot/saintsxctf/wmenstf",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json.get("self"), "/v2/groups/snapshot/saintsxctf/wmenstf"
        )
        self.assertEqual(response_json.get("group"), "/v2/groups/saintsxctf/wmenstf")
        self.assertIsNotNone(response_json.get("group_snapshot"))
        self.assertIn("members", response_json.get("group_snapshot"))
        self.assertIn("statistics", response_json.get("group_snapshot"))
        self.assertGreater(
            response_json.get("group_snapshot")["statistics"]["miles_all_time"], 0
        )
        self.assertGreater(
            response_json.get("group_snapshot")["statistics"]["run_miles_all_time"], 0
        )
        self.assertGreater(
            response_json.get("group_snapshot")["statistics"]["feel_all_time"], 0
        )

    def test_group_snapshot_by_group_name_get_route_200_expected_values(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/snapshot/<team_name>/<group_name>' route.  This test
        proves that retrieving a snapshot about a group with a valid group name results in the group with expected
        statistics values.
        """
        response: Response = self.client.get(
            "/v2/groups/snapshot/saintsxctf/wmensxc",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)

        statistics: dict = response_json.get("group_snapshot")["statistics"]
        self.assertEqual(25, statistics["miles_all_time"])
        self.assertEqual(3, statistics["run_miles_all_time"])
        self.assertEqual(8.7931, statistics["feel_all_time"])

        self.assertEqual(7, statistics["miles_past_week"])
        self.assertEqual(2, statistics["run_miles_past_week"])
        self.assertEqual(8.1429, statistics["feel_past_week"])

    def test_group_snapshot_by_group_name_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/groups/snapshot/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/snapshot/saintsxctf/wmenstf",
            AuthVariant.FORBIDDEN,
        )

    def test_group_snapshot_by_group_name_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/groups/snapshot/<team_name>/<group_name>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/groups/snapshot/saintsxctf/wmenstf",
            AuthVariant.UNAUTHORIZED,
        )

    def test_group_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/groups/links' route.  This test proves that calling
        this endpoint returns a list of other group endpoints.
        """
        response: Response = self.client.get("/v2/groups/links")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/groups/links")
        self.assertEqual(len(response_json.get("endpoints")), 14)
