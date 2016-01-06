%define url_ver %(echo %{version} | cut -d. -f1,2)

Name:		gnome-themes-standard
Version:	 3.18.0
Release:	4
Summary:	Standard themes for GNOME applications
Group:		Graphical desktop/GNOME
License:	LGPLv2+
Url:		http://git.gnome.org/browse/gnome-themes-standard
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-themes-standard/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	settings.ini
Source2:	gtkrc

BuildRequires:	intltool
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.5.17
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gdk-x11-2.0)
BuildRequires:	pkgconfig(librsvg-2.0)

# just for /usr/bin/gtk-update-icon-cache:
BuildRequires:	gtk+2.0

Requires:	gtk-engines2
Requires:	gnome-icon-theme
Requires:	abattis-cantarell-fonts
Requires:	adwaita-icon-theme
Requires:	adwaita-cursor-theme
Requires:	adwaita-gtk2-theme = %{version}-%{release}
Requires:	adwaita-gtk3-theme = %{version}-%{release}



%rename		gnome-background-standard
%rename		gnome-themes

%description
The gnome-themes-standard package contains the standard theme for the GNOME
desktop, which provides default appearance for cursors, desktop background,
window borders and GTK+ applications.

%package -n adwaita-gtk2-theme
Summary:	Adwaita gtk2 theme
Group:		Graphical desktop/GNOME

%description -n adwaita-gtk2-theme
The adwaita-gtk2-theme package contains a gtk2 theme for presenting widgets
with a GNOME look and feel.

%package -n adwaita-gtk3-theme
Summary:	Adwaita gtk3 theme
Group:		Graphical desktop/GNOME

%description -n adwaita-gtk3-theme
The adwaita-gtk3-theme package contains a gtk3 theme for rendering widgets
with a GNOME look and feel.

%prep
%setup -q

%build
%configure2_5x
#--disable-gtk2-engine
%make

%install
%makeinstall_std

install -Dpm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/gtk-3.0/settings.ini
install -Dpm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/gtk-2.0/gtkrc

%post
touch --no-create %{_datadir}/icons/Adwaita &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    for t in Adwaita HighContrast; do
        touch --no-create %{_datadir}/icons/$t &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/$t &>/dev/null || :
    done
fi

%posttrans
for t in Adwaita HighContrast; do
  gtk-update-icon-cache %{_datadir}/icons/$t &>/dev/null || :
done

%files
%doc NEWS README

# Background and WM
%{_datadir}/themes/Adwaita
%exclude %{_datadir}/themes/Adwaita/gtk-2.0
%exclude %{_datadir}/themes/Adwaita/gtk-3.0

# A11y themes
%{_datadir}/icons/HighContrast
%{_datadir}/themes/HighContrast

%files -n adwaita-gtk2-theme
# gtk2 Theme
%{_datadir}/themes/Adwaita/gtk-2.0
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so

# Default gtk2 settings
%config(noreplace) %{_sysconfdir}/gtk-2.0/gtkrc

%files -n adwaita-gtk3-theme
# gtk3 Theme and engine
%{_datadir}/themes/Adwaita/gtk-3.0

# Default gtk3 settings
%config(noreplace) %{_sysconfdir}/gtk-3.0/settings.ini

