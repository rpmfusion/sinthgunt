Name:           sinthgunt
Version:        2.0.3
Release:        3%{?dist}
Summary:        An easy to use GUI for ffmpeg
BuildArch:      noarch 
Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://code.google.com/p/sinthgunt
Source0:        http://sinthgunt.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:         sinthgunt_fix_desktop_file.patch
Requires:       ffmpeg pygtk2-libglade mplayer
# We must require the package that owns the directories where the icon file is
# being installed.
Requires:       hicolor-icon-theme
BuildRequires:  python-devel desktop-file-utils ImageMagick


%description
Sinthgunt is an open source graphical user interface for ffmpeg, a computer
program that can convert digital audio and video into numerous formats.
Using pre-configured conversion settings, it makes the task of converting
between different media formats very easy.


%prep
%setup -q
%patch0 -p1
chmod -x README.txt
chmod -x Sinthgunt/app.py
sed -i -e '/^#!\//, 1d' Sinthgunt/app.py


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/sinthgunt.desktop
rm -f $RPM_BUILD_ROOT%{_datadir}/sinthgunt/README.txt \
      $RPM_BUILD_ROOT%{_datadir}/sinthgunt/LICENSE.txt
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/sinthgunt.png

# Create square icons from logo file.
montage -crop +0+1 -background white -geometry +0+18 \
      $RPM_BUILD_ROOT%{_datadir}/sinthgunt/logo.png $RPM_BUILD_ROOT%{_datadir}/sinthgunt/icon.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps

convert -resize 48x48 $RPM_BUILD_ROOT%{_datadir}/sinthgunt/icon.png \
      $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/sinthgunt.png
cp $RPM_BUILD_ROOT%{_datadir}/sinthgunt/icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/sinthgunt.png


%files
%doc README.txt LICENSE.txt
%{_bindir}/sinthgunt
%{_bindir}/youtube-dl-sinthgunt
%{_datadir}/sinthgunt/
%{_datadir}/applications/sinthgunt.desktop
%{_datadir}/icons/hicolor/48x48/apps/sinthgunt.png
%{_datadir}/icons/hicolor/128x128/apps/sinthgunt.png
%{python_sitelib}/Sinthgunt/
%{python_sitelib}/sinthgunt-2.0.3-py2.7.egg-info


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Sat Feb 25 2012 Jean-Francois Saucier <jsaucier@gmail.com> - 2.0.3-3
- Fix the problem with icons and desktop file

* Tue Jan 10 2012 Jean-Francois Saucier <jsaucier@gmail.com> - 2.0.3-2
- Fix as per the suggestions on review #1034

* Tue Dec 28 2010 Jean-Francois Saucier <jsaucier@gmail.com> - 2.0.3-1
- Update to the new upstream version

* Mon Aug 23 2010 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 2.0.2-4
- Make some corrections as ask in #1034
- Fix Requires section

* Fri Mar 26 2010 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 2.0.2-3
- Fix some typos
- Add desktop-file-utils BuildRequires
- Remove shebang from non-executable-script

* Fri Jan 15 2010 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 2.0.2-2
- Fix the install and files section

* Mon Jan  4 2010 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 2.0.2-1
- Initial build for Fedora
