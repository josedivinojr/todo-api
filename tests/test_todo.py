from http import HTTPStatus

from app.models.todos import ToDoStatus
from tests.conftest import ToDoFactory


def test_create_todo(client, token):
    response = client.post(
        '/v1/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test ToDo',
            'description': 'Test ToDo Description',
            'status': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test ToDo',
        'description': 'Test ToDo Description',
        'status': 'draft',
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/v1/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/v1/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/v1/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, description='Desc Todo 1')
    )
    session.commit()

    response = client.get(
        '/v1/todos/?description=Desc',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_draft_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, status=ToDoStatus.draft)
    )
    session.commit()

    response = client.get(
        '/v1/todos/?status=draft',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            status=ToDoStatus.completed,
        )
    )

    session.bulk_save_objects(
        ToDoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            status=ToDoStatus.todo,
        )
    )
    session.commit()

    response = client.get(
        '/v1/todos/?title='
        'Test todo combined&description=combined&status=completed',
        headers={'Authorization': f'Bearer {token}'},
    )

    print(response.json())

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = ToDoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/v1/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/v1/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/v1/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, client, user, token):
    todo = ToDoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/v1/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
