# Metadata

This is a definition of the metadata files used within x86Launcher2.

Metadata files use the .ini format and are plain text. The metdata file itself is named **launch.dat** and stored in the game directory itself.

```
[default]
moby_id=
name=
developer=
publisher=
year=
rating=
genre=
series=
path=
start=
setup=
min_cpu=
min_ram=
video=
cover=
thumb=
screens=
beeper=
fm=
digifx=
midi=
```

An example metadata file may look as follows:

```
[default]
moby_id=299
name=Doom II
developer=id Software, Inc.
publisher=GT Interactive Software Corp.
year=1994
genre=Shooter
rating=8.2
series=Doom
path=C:\Games\Doom2
start=doom2.exe
setup=setup.exe
min_cpu=Intel i386 DX
min_ram=4 MB
video=EGA,VGA
cover=cover.bmp
thumb=covthumb.bmp
screens=screen1.bmp,screen2.bmp,screen3.bmp
beeper=0
fm=1
digifx=1
midi=1
```

In the case of the example above, the above metadata file would be in the following location:

   * C:\Games\Doom2\launch.dat

## Artwork Files

Artwork and other image assets are loaded from standard 8bpp Windows BMP files.

The following artwork files can be used:

   * Game box or cover artwork
     * 320x240, 8bpp
   * Game box or cover artwork thumbnail - for cover browser mode
     * 80x100, 8bpp
   * Screenshots
     * 320x240, 8bpp

Art which is loaded from the **server** metadata companion application is automatically resized and resampled down to 8bpp*.

All artwork is stored relative to the path of the game itself. In the case of the above example for Doom II, the art would be in the following locations:

   * C:\Games\Doom2\cover.bmp
   * C:\Games\Doom2\covthumb.bmp
   * C:\Games\Doom2\screen1.bmp
   * C:\Games\Doom2\screen2.bmp
   * C:\Games\Doom2\screen3.bmp

NOTE: Whilst the images are 8bpp, resampled images are **restricted to a maximum of 224 palette entries**, as 32 colours are reserved for use in the launcher user interface. The metadata server will automatically apply this colour restriction. 

Unmodified 8bpp artwork may be used, but will result in unsightly palette remapping of various user interface elements.