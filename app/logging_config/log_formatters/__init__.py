import logging
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.request_method = request.method
            record.request_path = request.path
        else:
            record.url = None
            record.remote_addr = None
            record.request_method = None
            record.request_path = None

        return super().format(record)
