from mangum import Mangum

from parimana.interfaces.web.main import app

handler = Mangum(app)
