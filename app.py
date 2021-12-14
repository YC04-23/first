from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

#钩子函数、g全局变量
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g,"user",user)
            g.user = user
        except:
            g.user = None


# 请求来了 -> before_request（绑定g） -> 视图函数 -> 视图函数中返回模板 -> context_processor 执行顺序
# 上下文处理器，渲染的所有模板都会显示这个user
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
