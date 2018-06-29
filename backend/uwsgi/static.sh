echo "---> Compiling static files..."
rm -rf /backend/static_root # Delete static files directory
django-admin collectstatic --pythonpath /backend/api <<<yes # Collect all static files
