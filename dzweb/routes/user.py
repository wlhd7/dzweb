from flask import Blueprint, render_template, request, session, g, redirect, url_for, flash, make_response, jsonify
from dzweb.db import get_db
from bcrypt import checkpw
from flask_babel import _
import json
from dzweb.routes.auth import login_required
from datetime import datetime, timedelta

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.before_request
@login_required
def load_added_apps():
    db = get_db()

    if g.user['applist']:
        applist = json.loads(g.user['applist'])
    else:
        applist = []

    g.applist = applist

    if applist:
        placeholder = ','.join(['?'] * len(applist))
        query = f'SELECT appname, appurl FROM apps WHERE id IN ({placeholder})'
        apps = db.execute(query, applist).fetchall()

        g.appname_appurl_dict = {app['appname']: app['appurl'] for app in apps}
    else:
        g.appname_appurl_dict = {}


@bp.route('/add-app', methods=['GET', 'POST'])
@login_required
def add_app():
    db = get_db()

    apps = db.execute(
            'SELECT * FROM apps',
        ).fetchall()

    if request.method == 'POST':
        app_number = request.form['number']
        app_password = request.form['password']
        stored_password = None

        for app in apps:
            try:
                if int(app['id']) == int(app_number):
                    stored_password = app['apppassword']
                    print(stored_password)
                    break
            except ValueError:
                flash('请输入应用ID (点击‘提示’查看应用ID)')

                return redirect(url_for('user.add_app'))

        if stored_password is None:
            flash('应用不存在')

            return render_template('user/add-app.html', apps=apps)

        check = checkpw(
                app_password.encode('utf-8'),
                stored_password.encode('utf-8')
            )

        if check:
            if app_number not in g.applist:
                g.applist.append(app_number)

                db.execute(
                        'UPDATE users SET applist = ? WHERE id = ?',
                        (json.dumps(g.applist), g.user['id'])
                    )
                db.commit()

                flash('应用添加成功')

                return redirect(url_for('user.add_app'))
            else:
                flash('该应用已经在应用列表中')
        else:
            flash('密码错误')

    return render_template('user/add-app.html', apps=apps)


@bp.route('/set-color', methods=['GET', 'POST'])
@login_required
def set_color():
    if request.method == "POST":
        color = request.form['color']
        db = get_db()

        db.execute(
                'UPDATE users SET color = ? WHERE id = ?',
                (color, g.user['id'])
            )
        db.commit()

        return redirect(url_for('user.set_color'))

    return render_template('user/set-color.html')


@bp.route('/weekend-overtime', methods=['GET', 'POST'])
@login_required
def weekend_overtime():
    cleanup_old_data()

    db = get_db()
    department = request.cookies.get('department', 'manu')

    # 获取日期参数
    date_str = request.args.get('date')

    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = datetime.now().date() + timedelta(days=1)
    else:
        current_date = datetime.now().date() + timedelta(days=1)

    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    column_name = current_date.strftime('%Y_%m_%d')

    # 计算前第七天的日期
    seven_days_ago = current_date - timedelta(days=7)
    seven_days_ago_column = seven_days_ago.strftime('%Y_%m_%d')

    # 标记是否使用了备用日期
    use_fallback_date = False
    fallback_date = None

    if request.method == 'POST':
        # 首先检查是否是 JSON 请求
        if request.content_type and 'application/json' in request.content_type:
            try:
                staff_data = request.get_json()
                if not staff_data:
                    return jsonify({'success': False, 'error': '无效的JSON数据'})

                action = staff_data.get('action')
                print(f"Received JSON action: {action}")  # 调试信息

                if action == 'add-date':
                    # 确保字段存在
                    try:
                        db.execute(f'ALTER TABLE staffs ADD COLUMN "{column_name}" TEXT DEFAULT "bg-1"')
                        db.commit()
                    except Exception as e:
                        print(f"Column issue: {e}")
                        db.rollback()

                    if 'staffs' in staff_data:
                        success_count = 0
                        for staff in staff_data['staffs']:
                            try:
                                result = db.execute(
                                    f'UPDATE staffs SET "{column_name}" = ? '
                                    'WHERE name = ? AND department = ?',
                                    (staff.get('status', 'bg-1'), staff['name'], staff['department'])
                                )
                                if result.rowcount > 0:
                                    success_count += 1
                                db.commit()
                            except Exception as e:
                                print(f"Error updating {staff['name']}: {e}")
                                db.rollback()
                                continue

                        print(f"Successfully updated {success_count} staff records")
                        return jsonify({'success': True, 'updated': success_count})

                    return jsonify({'success': False, 'error': '没有员工数据'})

            except Exception as e:
                db.rollback()
                print(f"JSON processing error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500

        # 处理表单请求（非JSON）
        action = request.form.get('action')
        print(f"Received form action: {action}")

        if action == 'department':
            department = request.form['department']
            resp = make_response(redirect(url_for('user.weekend_overtime', date=current_date.strftime('%Y-%m-%d'))))
            resp.set_cookie('department', department, max_age=365*24*3600)
            return resp

        elif action == 'add':
            name = request.form['name']
            sub_department = request.form.get('sub-department', 'none')

            try:
                db.execute(
                    'INSERT OR IGNORE INTO staffs (name, department, sub_department) VALUES (?, ?, ?)',
                    (name, department, sub_department)
                )
                db.commit()
            except Exception as e:
                print(f"Error adding staff: {e}")
                db.rollback()
            return redirect(url_for('user.weekend_overtime', date=current_date.strftime('%Y-%m-%d')))

        elif action == 'delete':
            name = request.form['name']
            try:
                db.execute('DELETE FROM staffs WHERE name = ?', (name,))
                db.commit()
            except Exception as e:
                print(f"Error deleting staff: {e}")
                db.rollback()
            return redirect(url_for('user.weekend_overtime', date=current_date.strftime('%Y-%m-%d')))

    # GET 请求处理
    try:
        # 确保当前日期字段存在
        db.execute(f'ALTER TABLE staffs ADD COLUMN "{column_name}" TEXT DEFAULT "bg-1"')
        db.commit()
    except Exception as e:
        print(f"Column creation issue: {e}")

    try:
        # 确保前第七天日期字段存在
        db.execute(f'ALTER TABLE staffs ADD COLUMN "{seven_days_ago_column}" TEXT DEFAULT "bg-1"')
        db.commit()
    except Exception as e:
        print(f"Seven days ago column creation issue: {e}")

    # 检查当前日期是否有加班记录（bg-2 或 bg-3）
    has_overtime = db.execute(
        f'SELECT COUNT(*) as count FROM staffs WHERE department = ? AND ("{column_name}" = "bg-2" OR "{column_name}" = "bg-3")',
        (department,)
    ).fetchone()['count'] > 0

    # 决定使用哪个日期的数据
    display_date = current_date
    display_column = column_name
    use_fallback_date = False

    if not has_overtime:
        # 检查前第七天是否有数据
        has_seven_days_data = db.execute(
            f'SELECT COUNT(*) as count FROM staffs WHERE department = ? AND ("{seven_days_ago_column}" = "bg-2" OR "{seven_days_ago_column}" = "bg-3")',
            (department,)
        ).fetchone()['count'] > 0

        if has_seven_days_data:
            display_date = seven_days_ago
            display_column = seven_days_ago_column
            use_fallback_date = True
            fallback_date = seven_days_ago

    # 获取要显示的数据
    staffs = db.execute(
        f'SELECT *, COALESCE("{display_column}", "bg-1") as current_status FROM staffs WHERE department = ?',
        (department,)
    ).fetchall()

    return render_template('user/weekend-overtime.html',
                         department=department,
                         staffs=staffs,
                         current_date=current_date,
                         display_date=display_date,  # 实际显示的日期
                         prev_date=prev_date,
                         next_date=next_date,
                         column_name=display_column,  # 实际使用的列名
                         use_fallback_date=use_fallback_date,
                         fallback_date=fallback_date)

def cleanup_old_data():
    """简化版：只在每月1号清理三个月前的数据"""
    today = datetime.now().date()

    # 只在每月前7天执行
    if today.day > 7:
        return 0

    db = get_db()
    try:
        # 清理三个月前的数据（保留两个月数据）
        three_months_ago = today - timedelta(days=90)

        columns = db.execute("PRAGMA table_info(staffs)").fetchall()
        column_names = [col[1] for col in columns]

        deleted_columns = []
        for column in column_names:
            if column.startswith('20') and len(column) == 10:
                try:
                    col_date = datetime.strptime(column, '%Y_%m_%d').date()
                    if col_date < three_months_ago:
                        db.execute(f'ALTER TABLE staffs DROP COLUMN "{column}"')
                        deleted_columns.append(column)
                        print(f"删除旧列: {column} (创建于 {col_date})")
                except ValueError:
                    continue

        db.commit()

        if deleted_columns:
            print(f"月度清理完成，共删除 {len(deleted_columns)} 个旧列")
        else:
            print("月度清理完成，无需删除任何列")

        return len(deleted_columns)

    except Exception as e:
        print(f"月度清理出错: {e}")
        db.rollback()
        return 0


@bp.route('/edit-produt-permisssion')
@login_required
def edit_product_permission():
    return render_template('user/edit-product-permission.html')


@bp.route('/edit-hir-permission')
@login_required
def edit_hire_permission():
    return render_template('user/edit-hire-permission.html')
