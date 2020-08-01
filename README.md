copy secrets file to separate dir and then set JWAPP_CONFD to be that dir.

mkdir ~/.config/jw/buildsight
cp conf.d/api/api_token.yaml ~/.config/jw/buildsight/
export JWAPP_CONFD=~/.config/jw/buildsight/
