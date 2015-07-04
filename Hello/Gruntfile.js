module.exports = function(grunt) {

  grunt.initConfig({
      pkg: grunt.file.readJSON('package.json'),

      dirs: {
        src: 'js/src'
        , flat: 'js/flat'
        , dest: 'js/min'
        , vendor: 'js/vendor'
      }

      , concat: {
          options: {
              separator: ';'
          }

          , all: {
              src: [
                  '<%= dirs.src %>/framework/stub.js'
                  , '<%= dirs.src %>/framework/adapter.js'
              ]
              , dest: '<%= dirs.flat %>/framework.js'
          }


          , vendor: {
              src: [
                  '<%= dirs.vendor %>/jquery-1.11.3.min.js'
                  , '<%= dirs.vendor %>/materalize.min.js'
                  , '<%= dirs.vendor %>/jsface/jsface.min.js'
                  , '<%= dirs.vendor %>/micro-events.js'
                  , '<%= dirs.vendor %>/jsface/jsface.pointcut.min.js'
                  , '<%= dirs.vendor %>/rivets.bundled.min.js'
                  , '<%= dirs.vendor %>/gator.min.js'
              ]
              , dest: '<%= dirs.flat %>/vendor.js'
          }

          , all_vendor: {
              src: [
                  '<%= concat.vendor.dest %>'
                  , '<%= concat.all.dest %>'
              ]

              , dest: '<%= dirs.flat %>/framework-vendor.js'
          }
      },

      uglify: {

          options: {
              banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
          },

          dist: {
              files: {
                  '<%= dirs.dest %>/vendor.min.js': ['<%= concat.vendor.dest %>']
                  , '<%= dirs.dest %>/<%= pkg.name %>.min.js': ['<%= concat.all.dest %>']
                  , '<%= dirs.dest %>/<%= pkg.name %>_vendor.min.js': ['<%= concat.all_vendor.dest %>']
              }
          }
      },

      jshint: {
          files: ['Gruntfile.js', 'src/**/*.js', 'test/**/*.js'],
          options: {
              // options here to override JSHint defaults
              globals: {
                  jQuery: true,
                  console: true,
                  module: true,
                  document: true
              }
          }
      },

      watch: {
          files: ['<%= jshint.files %>'],
          tasks: ['jshint']
      }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');

  grunt.registerTask('test', ['jshint']);

  grunt.registerTask('default', ['concat', 'uglify']);

};
