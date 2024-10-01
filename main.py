import os
from celery import Celery, Task
from celery import shared_task
from celery.result import AsyncResult
from dotenv import load_dotenv
from flask import Flask, jsonify, request


load_dotenv()
broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = os.getenv("CELERY_RESULT_BACKEND")


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)


app.config.from_mapping(
    CELERY=dict(
        broker_url=broker_url,
        result_backend=result_backend,
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


# Sample data (in-memory list)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    import time

    time.sleep(10)
    return a + b


@app.post("/add")
def start_add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = add_together.delay(a, b)
    return {"result_id": result.id}


@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
        "state": result.state,
    }


# Route to get all items (GET)
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
