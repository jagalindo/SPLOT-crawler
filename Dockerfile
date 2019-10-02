FROM python:3
ADD splot-crawl.py /
RUN pip install requests
RUN pip install urllib
RUN pip install bs4
CMD [ "python", "./splot-crawl.py" ]