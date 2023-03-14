import re

import pytest
import json
from pdfparse import app
from resources import SampleDocuments


@pytest.fixture()
def setup():
    app.config.update({'TESTING':True})


@pytest.fixture()
def client():
    return app.test_client()


def test_status_codes(client):
    response_no_file = client.put("/", data={})
    assert response_no_file.status_code == 400

    response_png = client.put("/", data={
        'file': SampleDocuments.image()
    })
    assert response_png.status_code == 400
    response_pdf = client.put("/", data={
        'file': SampleDocuments.basic()
    })
    assert response_pdf.status_code == 200


def test_pdf_mining(client):
    """Test for proper text parsing. Does not save any data."""
    response_1 = client.put("/", data={
        'file': SampleDocuments.basic(),
    })
    response_2 = client.put("/", data={
        'file': SampleDocuments.pet_rock(),
    })
    assert b"A Simple PDF File" in response_1.data
    assert any(
        "CONGRATULATIONS! \nYou are now the owner \nof a genuine, pedigreed \nPET ROCK."
        in re.sub(r" +", " ", chunk)
        for chunk in json.loads(response_2.data)
    )


def test_pdf_saving(client):
    """Test saving, accessing and deleting files.

    This will delete any documents saved.
    TODO: Make it keep previously saved documents
    """

    assert client.get('saved/sample.pdf').status_code == 404
    assert client.delete('saved/sample.pdf').status_code == 404

    # upload data
    response_1 = client.post("/", data={
        'file': SampleDocuments.basic(),
    })
    assert response_1.status_code == 200
    response_2 = client.post("/", data={
        'file': SampleDocuments.pet_rock(),
    })
    assert response_2.status_code == 200

    # check that data is saved
    saved_list_response = client.get("/saved")
    assert saved_list_response.status_code == 200
    saved_list = json.loads(saved_list_response.data)
    assert 'sample.pdf' in saved_list['known_files']
    assert 'pet_rock.pdf' in saved_list['known_files']

    # delete data
    for filename in saved_list['known_files']:
        get_response = client.get(f'saved/{filename}')
        assert get_response.status_code == 200, f"GET failed for {filename}, {get_response}"
        del_response = client.delete(f'saved/{filename}')
        assert del_response.status_code == 200, f"DELETE failed for {filename}, {del_response}"

    # check that no data remains
    empty_list_response = client.get("/saved")
    assert empty_list_response.status_code == 200
    assert len(json.loads(empty_list_response.data)['known_files']) == 0
