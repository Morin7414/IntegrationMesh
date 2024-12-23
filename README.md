echo "# IntegrationMesh" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Morin7414/IntegrationMesh.git
git push -u origin main




git remote add origin https://github.com/Morin7414/IntegrationMesh.git
git branch -M main
git push -u origin main


pip freeze > requirements.txt
This command will overwrite your existing requirements.txt file with the current list of installed packages and their versions.


reset migrations
https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
 python manage.py migrate --fake core zero

 gunicorn==21.2.0

 DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;