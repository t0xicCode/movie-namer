#!/usr/bin/ruby

require 'fileutils.rb'

puts "Movie Name Lister"
puts
puts "Current Directory: " + Dir.pwd

d = Dir.new(Dir.pwd).sort
formated = raw = 0
a = Array.new()

d.each {|x|
    next if x == '.' || x == '..'
    next if File.file?(x)
    if /^[^\.\[\]]+ \[\d{4}\]$/ =~ x then
        formated += 1
    else
        raw += 1
        a.push(x)
    end
}

puts "We have %d formated directories," % formated
puts "and %d raw directories." % raw


a.each {|x|
    puts
    puts "Directory: %s" % x
    print "Please choose (C)ontinue, (S)kip:"
    next if gets.chomp == "s"
    name = ""
    year = 0
    begin
        if name.empty? then
            name_match = /(.+).[\[\(\{]?\d{4}/.match(x)
            if name_match.nil? then
                name = ""
            else
                name = name_match.captures.pop.tr('.', ' ').chomp
            end
        end
        print "Name of the movie (%s): " % name
        namet = gets.chomp
        name = namet unless namet.empty?
        if year.zero? then
            year_match = /(\d{4})/.match(x)
            if year_match.nil? then
                year = ""
            else
                year = year_match.captures.pop.to_i
            end
        end
        print "Year (%s): " % year
        yeart = gets.chomp
        year = yeart.to_i unless yeart.empty?
                
        print "Renaming to '%s [%d]'. OK(Y/n)? " % [name, year]
    end while gets.chomp == 'n'
    
    files = Dir.glob(File.join(x, '*.{avi,mp4,mkv}')).sort
    (puts "No video file(s) found"; next) unless files.count > 0
    subs = Dir.glob(x + "*.{srt,idx,sub}").sort
    puts "%d subtitle file(s) found" % subs.count unless subs.count < 1
    
    if files.count > 1 then
        puts "There seems to be multiple video files."
        files.each_with_index {|f, i| puts "    (%d): %s" % [i, f]}
        print "Please select the main one: "
        file = files.slice!(gets.chomp.to_i)
    else
        file = files.pop
    end
    
    puts "Renaming video file"
    puts "    %s --> %s [%d]%s" % [File.basename(file) + File.extname(file), name, year, File.extname(file)]
    File.rename(file, "%s/%s [%d]%s" % [x, name, year, File.extname(file)])
    if subs.count > 0 then
    puts "Renaming subtitle files"
        subs.each {|s|
        puts "    %s --> %s [%d]%s" % [File.basename(s) + File.extname(s), name, year, File.extname(s)]
            File.rename(s, "%s/%s [%d]%s" % [x, name, year, File.extname(s)])
        }
    end
    puts "Renaming directory"
    puts "    %s --> %s [%d]" % [File.basename(x), name, year]
    FileUtils.mv( x, "%s/%s [%d]" % [File.expand_path('..', x), name, year])
}
