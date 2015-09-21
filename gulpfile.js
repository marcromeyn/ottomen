var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var less = require('gulp-less');
var minifyCSS = require('gulp-minify-css');
var browserify = require('browserify');
var es6ify = require('es6ify');
var reactify = require('reactify');
var envify = require('envify/custom');
var requireGlobify = require('require-globify');
var source = require('vinyl-source-stream');
var streamify = require('gulp-streamify');
var sourcemaps = require('gulp-sourcemaps');
var browserSync = require('browser-sync');

var paths = {
    scripts: './ottomen/web/frontend/react/js/',
    app_paths: './ottomen/web/frontend/react/js/**/*.*',
    vendor_styles: 'ottomen/web/frontend/react/css/*.css',
    less_styles: 'ottomen/web/frontend/react/less/*.less',
    css_styles: 'ottomen/web/frontend/react/css/*.css',
    templates: 'ottomen/web/frontend/templates/*.html'
};

var reload = browserSync.reload;
var process = require('child_process');

gulp.task('scripts', function () {
    es6ify.traceurOverrides = {experimental: true};

    browserify(paths.scripts+'development.js')
        .transform(reactify)
        .transform(es6ify)
        .transform(requireGlobify)
        .transform(envify())
        .bundle()
        .pipe(source('app.js'))
        //.pipe(streamify(sourcemaps.init()))
        .pipe(streamify(concat('app.min.js')))
        //    .pipe(uglify())
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('ottomen/web/frontend/static/dist/js'));
});

gulp.task('deploy', ['styles'], function () {
    es6ify.traceurOverrides = {experimental: true};

    return browserify(paths.scripts+'production.js')
        .transform(reactify)
        .transform(es6ify)
        .transform(envify())
        .bundle()
        .pipe(source('app.js'))
        //.pipe(streamify(sourcemaps.init()))
        .pipe(streamify(concat('app.min.js')))
        //    .pipe(uglify())
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('ottomen/web/frontend/static/dist/js'));
});

gulp.task('styles', function () {
    return gulp.src([paths.vendor_styles, paths.css_styles, paths.less_styles])
        .pipe(less())
        .pipe(concat('app.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest('ottomen/web/frontend/static/dist/css'));
});

//Run Flask server
gulp.task('runserver', function () {
    console.info('Starting flask server');
    var pipe = {stdio: 'inherit'};

    process.spawn('python', ['manage.py', 'runserver'], pipe);
});

gulp.task('watch', function () {
    gulp.watch(paths.app_paths, ['scripts']);
    gulp.watch(paths.css_styles, ['styles']);
});

// Default task: Watch Files For Changes & Reload browser
gulp.task('default', ['deploy'], ['runserver'], function () {
    browserSync({
        notify: false,
        proxy: "127.0.0.1:5003"
    });

});
