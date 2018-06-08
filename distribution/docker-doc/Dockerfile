FROM httpd:2.4
MAINTAINER iclientpy@supermap.com
ADD ./doc.tar /usr/local/apache2/htdocs/
ADD ./iclientpy-conda-package.tar /usr/local/apache2/htdocs/conda/
COPY ./icpy-tools.tar /usr/local/apache2/htdocs/downloads/
COPY ./icpy-tools.zip /usr/local/apache2/htdocs/downloads/