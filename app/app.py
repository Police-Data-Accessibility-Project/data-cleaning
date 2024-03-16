from flask import render_template, session, redirect, url_for, flash, request

from app.config import create_app
from app.models import db, DataEntry

app = create_app()
# Initialize the database

db.init_app(app)


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'DataEntry': DataEntry}


@app.route('/completion')
def completion():
    return render_template('completion.html')


# Create the database and tables
with app.app_context():
    db.create_all()


@app.route('/update_data', methods=['POST'])
def update_data():
    entry_id = request.form['entry_id']
    entry = DataEntry.query.get(entry_id)

    if request.form['action'] == 'accept':
        entry.old_url = request.form['new_value']
        flash('Change accepted.', 'success')
        entry.approved = True
    else:
        entry.approved = False
        entry.rejection_reason = 'duplicate'

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/')
def index():
    with app.app_context():
        if 'current_index' not in session:
            session['current_index'] = 0

        entry = DataEntry.query.filter(
            db.and_(
                DataEntry.possible_correct_url != '',
                DataEntry.approved.isnot(True),
                DataEntry.rejection_reason == ''
            )
        ).first()
        print(entry)
        if entry:
            return render_template('index.html', row=entry)
        else:
            session.pop('current_index', None)
            flash('All entries have been reviewed!', 'info')
            return redirect(url_for('completion'))


#

if __name__ == '__main__':
    # add_fake_data(20)
    print(app.root_path)
    app.run(debug=True)
