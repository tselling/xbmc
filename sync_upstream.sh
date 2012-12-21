#!/usr/bin/env bash

# Change dir to git clone
#cd ~/xbmc/xbmc.kmn

# Sync upstream/master
echo "Syncing upstream/master"
git checkout master || exit 1
git pull --rebase upstream master || exit 1
git push || exit 1

echo "Merging master onto origin/android-neon"
git checkout android-neon || exit 1
git merge origin/master || exit 1

echo "Merging master onto origin/android-neon-xaf-touch"
git checkout android-neon-xaf-touch || exit 1
git merge origin/master || exit 1

echo "Merging master onto origin/android-neon-xaf-set_top"
git checkout android-neon-xaf-set_top || exit 1
git merge origin/master || exit 1

echo "Merging master onto origin/android-tegra2"
git checkout android-tegra2 || exit 1
git merge origin/master || exit 1

echo "Merging master onto origin/android-tegra2-xaf-touch"
git checkout android-tegra2-xaf-touch || exit 1
git merge origin/master || exit 1

# Reset to android-neon branch
git checkout android-neon || exit 1
git push || exit 1

echo "Done"
