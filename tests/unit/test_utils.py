import pytest
from src.utils import eleva, requires_role
# from unittest.mock import patch
from http import HTTPStatus



@pytest.mark.parametrize("test_input,expected", [(2, 4), (4, 16), (9, 81)])
def test_eleva(test_input, expected):
    resultado = eleva(test_input)
    assert resultado == expected

@pytest.mark.parametrize("test_input,exc_class,msg", [("a",TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), (None, TypeError,"unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")])
def test_eleva_falha(test_input,exc_class,msg):
    with pytest.raises(exc_class) as exc:
        eleva(test_input)
    assert str(exc.value) == msg

def test_require_role_success(mocker):
   #given
   mock_user = mocker.Mock()
   mock_user.role.name = 'admin'

   mocker.patch('src.utils.get_jwt_identity')
   mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
   
   decorated_function = requires_role('admin')(lambda: "success")
   
   #when
   result = decorated_function()
   
   #then
   assert result == "success"

def test_require_role_fail(mocker):
   mock_user = mocker.Mock()
   mock_user.role.name = 'normal'

   mocker.patch('src.utils.get_jwt_identity')
   mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
   
   decorated_function = requires_role('admin')(lambda: "success")
   result = decorated_function()

   assert result == ({"msg": "Bad username or password"}, HTTPStatus.FORBIDDEN)
