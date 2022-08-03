from wtforms import Form, TextAreaField, validators, StringField

class CodeForm(Form):
    account = StringField('Account', [validators.DataRequired()])
    code = TextAreaField('Code',[validators.DataRequired()])


class DeployForm(Form):
    account = StringField('Account', [validators.DataRequired()])
    bytecode = TextAreaField('ByteCode',[validators.DataRequired()])
    abi = TextAreaField('ByteCode',[validators.DataRequired()])

    




