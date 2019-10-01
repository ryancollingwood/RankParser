from solver.variable_cleansor import clean_variable
from solver.variable_cleansor import match_variable


def test_can_call_clean_variable():
    try:
        clean_variable("")
    except NameError as e:
        raise e
    except:
        pass


def test_clean_variable_doesnt_modify_source():
    original = "Hello World"

    clean_variable(original)

    assert(original == "Hello World")


def test_clean_variable_result():
    original = "[Hello World]"
    expected = "Hello_World"

    result = clean_variable(original)
    assert(result == expected)


def test_can_call_match_variable():
    try:
        match_variable("cat", ("mouse", "house", "dog",))
    except NameError as e:
        raise e
    except:
        pass


def test_match_variable_with_empty_existing_matches():
    expected = "So_Lonely"
    result = match_variable("So Lonely", tuple())
    assert(result == expected)


def test_match_variable_gets_typo_match():
    typo = "Project managment"
    expected = "project_management"

    result = match_variable(typo, ("cat", "change_management", expected,), 95)

    assert(result == expected)


def test_match_variable_doesnt_false_positive_match():
    provided = "project management"
    expected = "project_management"

    result = match_variable(
        provided,
        (
            "it_project_management", "project_managers",
            "change_management", expected,
        ),
        10
    )

    assert(result == expected)


def test_match_variable_gets_fuzzy_match():
    expected = "house"
    result = match_variable("mouse", ("cat", "house", "dog",), 50)

    assert(result == expected)


def test_match_variable_gets_set_ratio():
    given = "walk the brown dog"
    expected = "walk_the_fuzzy_brown_dog"
    result = match_variable(
        given,
        (
            "clean brown house", "walk in the park",
            "eat pizza", expected
        ),
        90
    )

    assert(result == expected)
