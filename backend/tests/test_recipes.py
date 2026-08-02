def _recipe_payload(**overrides):
    payload = {
        "title": "にんじんのやわらか煮",
        "description": "離乳食後期から食べられる、やわらかく煮たにんじん。",
        "category": "side_dish",
        "ingredients": ["にんじん 1本", "だし汁 適量"],
        "instructions": ["にんじんをやわらかくゆでる", "細かく刻んでだし汁で煮る"],
        "cooking_time_minutes": 15,
        "servings": 2,
        "tags": ["離乳食", "後期"],
    }
    payload.update(overrides)
    return payload


class TestRecipeCreate:
    def test_create_recipe(self, client):
        response = client.post("/recipes", json=_recipe_payload())
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "にんじんのやわらか煮"
        assert data["category"] == "side_dish"
        assert data["ingredients"] == ["にんじん 1本", "だし汁 適量"]
        assert data["tags"] == ["離乳食", "後期"]
        assert data["is_public"] is True

    def test_create_recipe_requires_title(self, client):
        response = client.post("/recipes", json=_recipe_payload(title=""))
        assert response.status_code == 422

    def test_create_recipe_requires_category(self, client):
        response = client.post("/recipes", json=_recipe_payload(category=""))
        assert response.status_code == 422


class TestRecipeGet:
    def test_get_recipe(self, client):
        created = client.post("/recipes", json=_recipe_payload()).json()
        response = client.get(f"/recipes/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_get_nonexistent_recipe_returns_404(self, client):
        response = client.get("/recipes/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestRecipeSearch:
    def setup_method(self):
        self.recipes = [
            _recipe_payload(
                title="にんじんのやわらか煮",
                description="離乳食後期から食べられる、やわらかく煮たにんじん。",
                category="side_dish",
                ingredients=["にんじん", "だし汁"],
                tags=["離乳食", "後期"],
                cooking_time_minutes=15,
            ),
            _recipe_payload(
                title="鮭のムニエル",
                description="バターで香ばしく焼いた鮭のメイン料理。",
                category="main_dish",
                ingredients=["鮭", "バター", "小麦粉"],
                tags=["幼児食", "魚"],
                cooking_time_minutes=25,
            ),
            _recipe_payload(
                title="かぼちゃのポタージュ",
                description="かぼちゃの甘みがおいしいスープ。",
                category="soup",
                ingredients=["かぼちゃ", "牛乳", "玉ねぎ"],
                tags=["離乳食", "スープ"],
                cooking_time_minutes=30,
            ),
        ]

    def test_search_all(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes")
        assert response.status_code == 200
        assert response.json()["total"] == 3

    def test_search_by_keyword(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"keyword": "にんじん"})
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "にんじんのやわらか煮"

    def test_search_by_category(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"category": "main_dish"})
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "鮭のムニエル"

    def test_search_by_ingredients(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"ingredients": "かぼちゃ"})
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "かぼちゃのポタージュ"

    def test_search_by_tags(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"tags": "離乳食"})
        data = response.json()
        assert data["total"] == 2

    def test_search_by_max_cooking_time(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"max_cooking_time": 20})
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "にんじんのやわらか煮"

    def test_search_combined_filters(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get(
            "/recipes",
            params={"tags": "離乳食", "max_cooking_time": 20},
        )
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "にんじんのやわらか煮"

    def test_search_pagination(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"per_page": 2})
        data = response.json()
        assert data["total"] == 3
        assert data["total_pages"] == 2
        assert len(data["recipes"]) == 2

        response = client.get("/recipes", params={"per_page": 2, "page": 2})
        data = response.json()
        assert len(data["recipes"]) == 1

    def test_search_no_results(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        response = client.get("/recipes", params={"keyword": "存在しないレシピ"})
        data = response.json()
        assert data["total"] == 0
        assert data["recipes"] == []

    def test_search_returns_public_recipes_only(self, client):
        for recipe in self.recipes:
            client.post("/recipes", json=recipe)
        draft = client.post("/recipes", json=_recipe_payload(title="下書き")).json()
        client.patch(f"/recipes/{draft['id']}", json={"is_public": False})
        response = client.get("/recipes")
        assert response.json()["total"] == 3


class TestRecipeUpdate:
    def test_update_recipe(self, client):
        created = client.post("/recipes", json=_recipe_payload()).json()
        response = client.patch(
            f"/recipes/{created['id']}",
            json={"title": "更新後のタイトル", "category": "main_dish"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新後のタイトル"
        assert data["category"] == "main_dish"

    def test_update_nonexistent_recipe_returns_404(self, client):
        response = client.patch(
            "/recipes/00000000-0000-0000-0000-000000000000",
            json={"title": "タイトル"},
        )
        assert response.status_code == 404


class TestRecipeDelete:
    def test_delete_recipe(self, client):
        created = client.post("/recipes", json=_recipe_payload()).json()
        response = client.delete(f"/recipes/{created['id']}")
        assert response.status_code == 204

        response = client.get(f"/recipes/{created['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_recipe_returns_404(self, client):
        response = client.delete("/recipes/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
