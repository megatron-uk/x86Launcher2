# x86Launcher2
Next iteration of the x86Launcher for DOS game browsing/launching on native retro hardware.

This version of x86Launcher2 improves on the original concept by having support for metadata pulled directly from Mobygames.

Consider it equivalent to EmulationStation, Launchbox or Retroarch, but instead running on real retro hardware.

### Why x86Launcher2?

The original [x86Launcher](https://github.com/megatron-uk/x86Launcher) was one of the first graphical applications I wrote for DOS several years ago. I've made several improvements in codebase since then, and it has a number of restrictions that mean it is not practical to take it any further. 

Starting from scratch was the only realistic option.

## Client

The client applications runs on a real **DOS PC**, presents a catalogue of your games, artwork and metadata, and allows you to search through and launch any of the titles in your catalogue.

The **user interface client** is written in C, using GCC/DJGPP for IBM PC systems of the following specs:

   * 386 and above
   * 4MB of RAM
   * Hard disk or other solid state drive (e.g. SD/CF)
   * VGA adapter with at least VESA 1.2 support
   * VGA must support 640x480 256 colour

A **metadata scraper client** is also written in C, using GCC/DJGPP and requires the following:

   * 386 and above
   * 4MB of RAM
   * Hard disk or other solid state drive (e.g. SD/CF)
   * Network card with DOS packet driver

The scraper client communicates with the server application to make requests to Mobygames for game data and artwork. It is not needed to run the user interface or to launch games. You can enter details manually in the metadata files for each game if you wish.

## Server

The server application runs on a **modern PC** (either Windows/Linux/Mac) and serves as a proxy for the client to make queries to the Mobygames library, and to retrieve and resample artwork before sending it back to the client.

The server is written in Python, requiring Python 3.x.

The server is an optional component - metadata and image artwork can be added to the client entirely manually, if necessary. 

## Metadata

Details for each game (name, release date, genre, artwork filenames) are stored in a metadata file within the game directory.

The metadata file is documented [here](metadata.md).