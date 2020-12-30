#!/usr/bin/env python3

from subprocess import run, Popen, PIPE, DEVNULL
import shlex
import os


def makeTar(appDir, targetDir, name):
  backupDir = os.path.join(appDir, "data")

  cmd = f"/bin/tar --numeric-owner -cp -f {backupDir}/{name}.tar {targetDir}"

  run(shlex.split(cmd))


def dumpDatabase(appDir, dbname):
  backupDir = os.path.join(appDir, "data")
  sqlFile = f"{dbname}.sql"
  backupFilePath = os.path.join(backupDir, sqlFile)
  mysqlCfgFn = f"{dbname}.cfg"
  mysqlCfgPath = os.path.join(appDir, "script", mysqlCfgFn)

  cmd = f"/usr/bin/mysqldump --defaults-file={mysqlCfgPath} {dbname}"
  p = Popen(shlex.split(cmd), shell=False, stdout=PIPE, stderr=DEVNULL)

  with open(backupFilePath, "wb") as f:
    f.writelines(p.stdout)

def clearBackupDir(appDir):
  backupDir = os.path.join(appDir, "data")

  cmd = f"/bin/rm -fr {backupDir}/*"
  run(cmd, shell=True)


if __name__ == '__main__':
  appDir = "/opt/backup"

  clearBackupDir(appDir)
  makeTar(appDir, "/var/www/moodle", "moodle")
  makeTar(appDir, "/var/www/moodledata", "moodledata")
  dumpDatabase(appDir, "moodle")