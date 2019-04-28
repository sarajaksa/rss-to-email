# RSS to Email Script

This is a script, that checks all the RSS feeds and then sends all the new posts in one email or sends an empty one, if there is no new posts. 

The motivation for this was, that I noticed that sometimes, I circle over 3-4 sites, when I want to procrastinate. This was creates as a sort of way, if the urge would be smaller, if I got an email every day, that there is nothing new there. 

## Getting Started

In order for the program to work, a person needs to put the authentication information in the file stable.py. The program so far assumes that the email address is also the username. The folder with settings (rss-links.txt and time.txt) can also be adjusted there.

All the RSS feeds to check are put in the file rss-links.txt, with each feed in its own line. 

In Arch Linux, the scheduling can be done with [Timers](https://wiki.archlinux.org/index.php/Systemd/Timers). 
