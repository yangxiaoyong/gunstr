#!/usr/bin/env bash

rails docs_app
cd docs_app
rake rails:freeze:gems
echo > vendor/rails/activesupport/README
rake doc:rails
