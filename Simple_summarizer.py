from flask import Flask, request, render_template
from gensim.summarization.summarizer import summarize
from wtforms import Form, FloatField, validators, TextAreaField

app = Flask(__name__)


class InputForm(Form):
    ratio = FloatField(
        label='Ratio (0.1-0.99)', default=0.3,
        validators=[validators.InputRequired(),
                    validators.NumberRange(0.1, 0.99, 'Ratio must be between 0.1 and 0.99')])
    text = TextAreaField(
        label='Text', default='',
        validators=[validators.InputRequired(), validators.Length(100, message="Text must be at least 100 characters")]
    )


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InputForm(request.form)
    if request.method == 'GET':
        return render_template('summary_app_index.html', form=form)
    if request.method == 'POST' and form.validate():
        ratio = form.ratio.data
        text = form.text.data
        print('ratio used: ', ratio)
        print('predicting...')
        prediction = predict(text, ratio)
        print('prediction done')
        print(prediction)
        return render_template('summary_app_output.html', form=form, prediction=prediction, text=text)
    else:
        return render_template('summary_app_index.html', form=form)


def predict(text, ratio):
    return summarize(text, ratio)


if __name__ == "__main__":
    app.run()
