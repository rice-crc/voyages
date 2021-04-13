#!/bin/sh

if grep -q 'blue' ~/.sv_env
then
  old_env='blue'
  old_port='8000'
  new_env='green'
  new_port='8001'
else
  old_env='green'
  old_port='8001'
  new_env='blue'
  new_port='8000'
fi

declare -a instances=(
   "app01"
   "app02"
)

for instance in "${instances[@]}"; do
  echo "[sv-${instance}] Building ${new_env}"
  docker-compose --context $instance -f docker-compose.prod.yml up -d --no-deps --build voyages-django-${new_env}

  echo "[sv-${instance}] Updating Nginx upstream and restarting"
  docker-compose --context $instance -f docker-compose.prod.yml exec voyages-nginx bash -c "sed -ie 's/-${old_env}:${old_port}/-${new_env}:${new_port}/' /etc/nginx/conf.d/voyages.conf"
  docker-compose --context $instance -f docker-compose.prod.yml exec voyages-nginx nginx -s reload

  echo "[sv-${instance}] Removing ${old_env}"
  docker-compose --context $instance -f docker-compose.prod.yml rm --stop --force voyages-django-${old_env}
done

echo $new_env > ~/.sv_env
echo "Production is now ${new_env}"

echo "[sv-${instances[0]}] Running asset tasks"
docker-compose --context ${instances[0]} -f docker-compose.prod.yml exec voyages-django-${new_env} bash -c 'python manage.py compilemessages'
docker-compose --context ${instances[0]} -f docker-compose.prod.yml exec voyages-django-${new_env} bash -c 'python manage.py compilescss'
docker-compose --context ${instances[0]} -f docker-compose.prod.yml exec voyages-django-${new_env} bash -c 'python manage.py collectstatic --noinput'
docker-compose --context ${instances[0]} -f docker-compose.prod.yml exec voyages-django-${new_env} bash -c 'python manage.py compress --force'
docker-compose --context ${instances[0]} -f docker-compose.prod.yml exec voyages-django-${new_env} bash -c 'python manage.py thumbnail cleanup'
