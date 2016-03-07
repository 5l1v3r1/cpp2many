
###############################################################################
# system requires
###############################################################################

debug = require("debug") "jutge-cpp2many"
express = require "express"
path = require "path"
favicon = require "serve-favicon"
logger = require "morgan"
cookieParser = require "cookie-parser"
bodyParser = require "body-parser"
fs = require "fs"
childProcess = require "child_process"
uuid = require 'node-uuid'
moment = require 'moment'
expandHomeDir = require 'expand-home-dir'

###############################################################################
# Constants
###############################################################################

dat = expandHomeDir '~/dat/submissions'



###############################################################################
# Routers
###############################################################################


index = (req, res, next) ->
    res.render 'index',
        title: 'cpp2many'
        uuid: uuid.v4().replace /-/g, ''


submit = (req, res, next) ->

    extensions =
        pascal: '.pas'
        python: '.py'
        ada   : '.ada'
        java  : '.java'

    id = req.params.id
    code = req.body.code.replace /\r/g, ''
    lang = req.body.lang
    ext = extensions[lang]
    json = dat+'/'+id+'.json'
    input = dat+'/'+id+'.cc'
    output = dat+'/'+id+ext
    error = dat+'/'+id+'.err'

    meta =
        lang: lang
        time: moment().format 'YYYY-MM-DD hh:mm:ss'
        ip: req.connection.remoteAddress
        ext: ext

    if not id.match /^\w+$/
        res.render 'myerror',
            title: 'cpp2many'
            msg: 'Invalid submission.'
        return
    if not lang.match /^\w+$/
        res.render 'myerror',
            title: 'cpp2many'
            msg: 'Invalid language.'
        return
    if code.length > 64*1024
        res.render 'myerror',
            title: 'cpp2many'
            msg: 'Program too long.'
        return

    fs.access json, fs.F_OK, (stat) ->
        if not stat
            # the json file exists
            res.render 'myerror',
                title: 'cpp2many'
                msg: 'Submission already exists.'
        else
            # the json file does not exist
            fs.writeFile json, JSON.stringify(meta, null, 2),  (err) ->
                fs.writeFile input, code,  (err) ->
                    cmd = "cd #{dat} ; #{__dirname}/../PoliCmm/src/PoliCmm.py --#{lang} #{id}.cc 2> #{id}.err"
                    childProcess.exec cmd, (err, stdout, stderr) ->
                        submission req, res, next


submission = (req, res, next) ->

    id = req.params.id
    json = dat+'/'+id+'.json'
    input = dat+'/'+id+'.cc'
    error = dat+'/'+id+'.err'

    if not id.match /^\w+$/
        res.render 'myerror',
            title: 'cpp2many'
            msg: 'Invalid submission.'
        return


    fs.access json, fs.F_OK, (stat) ->
        if stat
            # the json file does not exist
            res.render 'myerror',
                title: 'cpp2many'
                msg: 'Submission does not exist.'
        else
            # the json file exists
            fs.readFile json, (e, meta) ->
                json = JSON.parse meta
                fs.readFile input, encoding: 'utf-8', (e, inp) ->
                    output = dat+'/'+id+json.ext
                    fs.readFile output, encoding: 'utf-8', (e, out) ->
                        fs.readFile error, (e, err) ->
                            res.render 'submission',
                                title: 'Submission ' + id
                                inp: inp
                                out: out
                                err: err
                                meta: meta



###############################################################################
# Application
###############################################################################

# create the express app
app = express()


app.use bodyParser.json()
app.use bodyParser.urlencoded
    extended: true


# view engine setup
app.set "views", path.join __dirname, "views"
app.set "view engine", "jade"

# generate javascripts from coffeescripts on the fly for the client
app.use require("connect-coffee-script")
    src    : "#{__dirname}/client"
    dest   : "#{__dirname}/public/javascripts"
    prefix : "/javascripts"

app.use favicon "#{__dirname}/public/favicon.ico"

app.use logger "dev"
app.use cookieParser()
app.use require("stylus").middleware path.join __dirname, "public"



# set static paths
app.use express.static path.join __dirname, "public"
app.use "/bower_components", express.static path.join __dirname, "bower_components"


# set routers
app.get '/', index
app.get '/:id', submission
app.post '/:id', submit


# catch 404 and forward to error handler
app.use (req, res, next) ->
    err = new Error "Not Found"
    err.status = 404
    next err


# development error handler
# will print stacktrace
if app.get("env") is "development"
    app.use (err, req, res, next) ->
        res.status err.status or 500
        res.render "error",
            message: err.message,
            error: err


# production error handler
# no stacktraces leaked to user
app.use (err, req, res, next) ->
    res.status err.status or 500
    res.render "error",
        message: err.message,
        error: {}


# pretty print html
if app.get("env") is "development"
    app.locals.pretty = true




###############################################################################
# exports
###############################################################################

module.exports = app

