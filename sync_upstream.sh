#!/usr/bin/env bash

# Change dir to git clone
#cd ~/xbmc/xbmc.kmn

# Sync upstream/master
echo "Syncing upstream/master"
git checkout master
git pull --rebase upstream master
git push

echo "Merging master onto origin/android-neon"
git checkout android-neon
git merge origin/master

echo "Merging master onto origin/android-neon-xaf-touch"
git checkout android-neon-xaf-touch
git merge origin/master

echo "Merging master onto origin/android-tegra2"
git checkout android-tegra2
git merge origin/master

echo "Merging master onto origin/android-tegra2-xaf-touch"
git checkout android-tegra2-xaf-touch
git merge origin/master

# Reset to android-neon branch
git checkout android-neon
git push

echo "Done"
