var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var less = require('gulp-less');
var minifyCSS = require('gulp-minify-css');
var browserify = require('browserify');
var es6ify = require('es6ify');
var reactify = require('reactify');
var source = require('vinyl-source-stream');
var streamify = require('gulp-streamify');
var sourcemaps = require('gulp-sourcemaps');
var browserSync = require('browser-sync');

var paths = {
    scripts: './ottomen/web/frontend/static/js/app.js',
    app_paths: './ottomen/web/frontend/static/js/**/*.*',
    vendor_styles: 'ottomen/web/frontend/static/css/*.css',
    styles: 'ottomen/web/frontend/static/less/*.less',
    templates: 'ottomen/web/frontend/templates/*.html'
};

var reload = browserSync.reload;
var process = require('child_process');

gulp.task('scripts', function () {
    es6ify.traceurOverrides = {experimental: true};

    return browserify(paths.scripts)
        .transform(reactify)
        .transform(es6ify)
        .bundle()
        .pipe(source('app.js'))
        //.pipe(streamify(sourcemaps.init()))
        .pipe(streamify(concat('app.min.js')))
        //    .pipe(uglify())
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('ottomen/web/frontend/static/dist/js'));
});

gulp.task('styles', function () {
    return gulp.src([paths.vendor_styles, paths.styles])
        .pipe(less())
        .pipe(concat('app.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest('ottomen/web/frontend/static/dist/css'));
});

//Run Flask server
gulp.task('runserver', function () {
    console.info('Starting flask server');
    //var virtualenv = '/Users/marcromeyn/.virtualenvs/reactflask/bin/python';
    var pipe = {stdio: 'inherit'};

    process.spawn('python', ['manage.py', 'runserver'], pipe);
});

gulp.task('watch', function () {
    gulp.watch(paths.app_paths, ['scripts']);
    gulp.watch(paths.styles, ['styles']);
});

// Default task: Watch Files For Changes & Reload browser
gulp.task('default', ['runserver'], function () {
    browserSync({
        notify: false,
        proxy: "127.0.0.1:5003"
    });

    gulp.watch(paths.app_paths, ['scripts', reload]);
    gulp.watch(paths.styles, ['styles', reload]);
    gulp.watch(paths.templates, reload);

    //gulp.watch(['templates/*.*'], reload);

});
