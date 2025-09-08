from flask import request, url_for

def paginate_query(query, page_arg='page', per_page=12):
    page = request.args.get(page_arg, 1, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}
