git config --global user.name $GH_USERNAME
git config --global user.email $GH_MAIL
git clone https://github.com/$GITHUB_REPOSITORY repo
mv config.json repo/config.json
cd repo || exit 1
git add config.json
git commit -m "Update Accounts Password"
git push -q https://$GH_TOKEN@github.com/$GITHUB_REPOSITORY HEAD:main
