const fs = require('fs-extra')
const AWS = require('aws-sdk')
const gitP = require('simple-git/promise')

const s3 = new AWS.S3()

const { tempDir, gitRepo } = require('./config')

const { GH_KEY, GH_USER, GH_EMAIL, S3_BUCKET } = process.env

const gitDir = `${tempDir}/git`

const getFileFromS3 = (filename) =>
  new Promise((resolve, reject) => {
    const params = {
      Bucket: S3_BUCKET,
      Key: filename
    }
    s3.getObject(params, (err, data) => {
      if (err) {
        reject(err)
      } else {
        resolve(data)
      }
    })
  })

const writeS3ObjectToFile = (obj, filePath) =>
  new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filePath)
    file.write(obj.Body, (err) => {
      if (err) {
        reject(err)
      } else {
        file.end()
        resolve()
      }
    })
  })

const filterMovies = (notifiedMovies) =>
  new Promise((resolve, reject) => {
    fs.readJSON(`${gitDir}/movies.json`)
      .then(moviesRepository => {
        const moviesList = Object.keys(moviesRepository)

        const waitList = moviesList
          .filter(movie => notifiedMovies.indexOf(movie) === -1)
          .reduce((obj, key) => {
            obj[key] = moviesRepository[key]
            return obj
          }, {})
        const notified = moviesList
          .filter(movie => notifiedMovies.indexOf(movie) > -1)
          .reduce((obj, key) => {
            obj[key] = moviesRepository[key]
            return obj
          }, {})

        return fs.writeFile(`${gitDir}/movies.json`, JSON.stringify(waitList, null, 2))
          .then(() => fs.writeFile(`${gitDir}/notified.json`, JSON.stringify(notified, null, 2)))
      })
      .then(resolve)
      .catch(reject)
  })

module.exports.clearNotified = (event, content, callback) => {
  const repoURL = `https://${GH_KEY}@github.com/${gitRepo}`

  fs.mkdirp(gitDir)
    .then(() => {
      const git = gitP(gitDir)
      return git.init()
        .then(() => git.addConfig('user.name', GH_USER))
        .then(() => git.addConfig('user.email', GH_EMAIL))
        .then(() => git.addRemote('origin', repoURL))
        .then(() => git.pull('origin', 'master'))
        .then(() => getFileFromS3('notified.txt'))
        .then(file => {
          const notifiedMovies = file.Body.toString().split('\n')
          return filterMovies(notifiedMovies)
        })
        .then(() => git.add('./'))
        .then(() => git.commit('[AWS:Lambda] Update Notified'))
        .then(() => git.push('origin', 'master'))
    })
    .then(() => {
      console.log(`[GIT]: ${gitRepo} updated`)
      callback(null, {
        success: true
      })
    })
    .catch(callback)
}
