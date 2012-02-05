#define svn_rev 3058

Name:    qbittorrent
Summary: A Bittorrent Client 
Version: 2.8.1
Release: 1%{?dist}.R
Epoch:   1
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn checkout -r %{svn_rev} https://qbittorrent.svn.sourceforge.net/svnroot/qbittorrent/trunk qbittorrent
# rm -rf qbittorrent/.svn
# tar -czvf qbittorrent-%{svn_rev}svn.tar.gz qbittorrent
#Source0:  %{name}-%{svn_rev}svn.tar.gz
Source0: http://downloads.sf.net/qbittorrent/%{name}-%{version}.tar.gz
#Source0: http://downloads.sourceforge.net/project/qbittorrent/qbittorrent-unstable/%{name}-%{version}rc3.tar.gz
Source1: qbittorrent-nox.README
Patch0:  disable_extra_debug.patch

# Upstream patches

URL: http://sourceforge.net/projects/qbittorrent
Group: Applications/Internet
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: GPLv2+
BuildRequires: qt4-devel
BuildRequires: desktop-file-utils
BuildRequires: boost-devel
BuildRequires: asio-devel
BuildRequires: rb_libtorrent-devel >= 0.14.4
BuildRequires: glib2-devel
BuildRequires: libnotify-devel
BuildRequires: GeoIP-devel
BuildRequires: qtsingleapplication-devel


%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}

%description
A Bittorrent client using rb_libtorrent and a Qt4 Graphical User Interface.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%package nox
Summary: A Headless Bittorrent Client
Group: Applications/Internet
BuildRequires: qtsinglecoreapplication-devel

%description nox
A Headless Bittorrent client using rb_libtorrent.
It aims to be as fast as possible and to provide multi-OS, unicode support.

%prep
%setup -q
rm -rf src/qtsingleapp
#%patch0 -p1 -b .disable_extra_debug
# Upstream patches


cp -p %{SOURCE1} .

%build
# use ./configure instead of %%configure as it doesn't work
# configure and make headless first
mkdir -p build-nox
cd build-nox
../configure --prefix=%{_prefix} --disable-gui --with-qtsingleapplication=system
cp conf.pri ..
make %{?_smp_mflags}
mv -f ../conf.pri ../conf.pri.nox
# configure and make gui version
cd ..
mkdir -p build-gui
cd build-gui
../configure --prefix=%{_prefix}  --with-qtsingleapplication=system
cp conf.pri ..
make %{?_smp_mflags}
mv -f ../conf.pri ../conf.pri.gui


%install
rm -rf $RPM_BUILD_ROOT
# install headless version
mv -f conf.pri.nox conf.pri
cd build-nox
make INSTALL_ROOT=$RPM_BUILD_ROOT install
# install gui version
cd ..
mv -f conf.pri.gui conf.pri
cd build-gui
make INSTALL_ROOT=$RPM_BUILD_ROOT install


desktop-file-install \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications/ \
  --delete-original \
        $RPM_BUILD_ROOT%{_datadir}/applications/qBittorrent.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-, root, root, -)
%doc README NEWS COPYING AUTHORS TODO Changelog
%{_mandir}/man1/qbittorrent.1*
%{_bindir}/qbittorrent
%{_datadir}/applications/qBittorrent.desktop
%{_datadir}/icons/hicolor/*/apps/qbittorrent.png
%{_datadir}/pixmaps/qbittorrent.png

%files nox
%defattr(-,root,root,-)
%doc qbittorrent-nox.README NEWS COPYING AUTHORS TODO Changelog
%{_bindir}/qbittorrent-nox
%{_mandir}/man1/qbittorrent-nox.1*


%changelog
* Sun Feb  5 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 1:2.8.1-1.R
- rebuilt

* Sun Jun 05 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.1-1
- update to 2.8.1

* Thu Jun 02 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-1
- update to 2.8.0

* Fri May 27 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.8.rc3
- update to 2.8.0rc3

* Sun May 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.7.rc2
- update to 2.8.0rc2

* Sun May 22 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.6.rc1
- update to 2.8.0rc1

* Wed May 04 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.5.beta5
- update to 2.8.0beta5

* Mon Apr 18 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.4.beta4
- update to 2.8.0beta4

* Sat Apr 16 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.3.beta3
- update to 2.8.0beta3

* Mon Apr 11 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.2.beta2
- update to 2.8.0beta2

* Sat Apr 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-0.1.beta1
- update to 2.8.0beta1

* Thu Apr 07 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.2-1
- update to 2.7.2

* Wed Apr 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.1-1
- update to 2.7.1

* Sun Mar 20 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-1
- update to 2.7.0 release

* Wed Mar 16 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.6.rc1
- update to 2.7.0rc1

* Sun Mar 13 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.5.beta4
-  update to 2.7.0beta4

* Sat Mar 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.4.beta3
-  update to 2.7.0beta3

* Thu Mar 03 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.3.beta2
-  update to 2.7.0beta2

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1:2.7.0-0.2.beta1
- Rebuild against new rb_libtorrent

* Wed Feb 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.7.0-0.1.beta1
-  update to 2.7.0beta1

* Wed Feb 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.6-1
-  update to 2.6.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.5-2
- drop boost_filesystem v2 patch (bug 654807)

* Sat Feb 05 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.5-1
-  update to 2.6.5
-  rebuilt and patched for boost changes

* Thu Jan 27 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.4-2
- rebuilt

* Sun Jan 23 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.4-1
-  update to 2.6.4

* Sat Jan 15 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.3-1
-  update to 2.6.3

* Wed Jan 12 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.2-1
- update to 2.6.2

* Mon Jan 10 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.1-1
- update to 2.6.1

* Sun Jan 09 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-1
- update to 2.6.0 release

* Thu Jan 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-0.6.rc2
- update to 2.6.0rc2

* Thu Jan 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-0.5.rc1
- update to 2.6.0rc1

* Sat Jan 01 2011 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.4.beta4
- update to 2.6.0beta4

* Sun Dec 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.3.beta3
- update to 2.6.0beta3

* Sat Dec 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.2.beta2
- update to 2.6.0beta2

* Sun Dec 19 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.6.0-0.1.beta1
- update to 2.6.0beta1

* Sun Dec 05 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.1-1
- update to 2.5.1

* Sun Dec 05 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-1
- update to 2.5.0 release

* Mon Nov 29 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.12.rc4
- update to 2.5.0rc4

* Mon Nov 29 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.11.rc3
- update to 2.5.0rc3

* Thu Nov 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.10.rc2
- update to 2.5.0rc2

* Tue Nov 23 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.9.rc1
- update to 2.5.0rc1

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.8.beta7
- update to 2.5.0beta7

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.7.beta6
- replaced wrongly versioned source code

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.6.beta6
- update to 2.5.0beta6

* Sun Nov 21 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.5.beta5
- update to 2.5.0beta5

* Thu Nov 18 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.4.beta4
- update to 2.5.0beta4
- add temp build fix

* Sat Nov 13 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.3.beta3
- update to 2.5.0beta3

* Sat Nov 06 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.2.beta2
- rebuilt and patched for new libnotify version

* Mon Oct 25 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.5.0-0.1.beta2
- update to 2.5.0beta2

* Sun Oct 24 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.8-1
- update to 2.4.8

* Mon Oct 18 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.6-1
- update to 2.4.6

* Sat Oct 02 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.4-1
- update to 2.4.4

* Mon Sep 27 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.3-1
- update to 2.4.3

* Sun Sep 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.2-1
- update to 2.4.2
- drop qt_deprecated patch as it was merged upstream

* Sun Sep 26 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.1-1
- update to 2.4.1

* Mon Aug 30 2010 leigh scott <leigh123linux@googlemail.com> - 1:2.4.0-2
- rebuilt

* Tue Aug 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- update to 2.4.0 release

* Mon Aug 23 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.6.rc3
- update to 2.4.0rc3

* Sat Aug 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.5.rc2
- update to 2.4.0rc2

* Fri Aug 20 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.4.rc1
- update to 2.4.0rc1

* Fri Aug 20 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.3.beta3
- drop upstream missing includes patch
- update to 2.4.0beta3

* Thu Aug 19 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.2.beta2
- add upstream missing includes patch
- update to 2.4.0beta2

* Tue Aug 17 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.1.beta1
- drop upstream patches
- update to 2.4.0beta1

* Fri Aug 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-3
- remove temporary gcc45 patch and replace with upstream fix

* Fri Jul 30 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-2
- rebuild for new boost version
- add gcc45 patch (temporary patch till it's fixed properly)

* Tue Jul 27 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-1
- update to 2.3.0 final

* Sun Jul 25 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.13.rc10
- update to 2.3.0rc10

* Sat Jul 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.12.rc9
- update to 2.3.0rc9

* Fri Jul 23 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.11.rc8
- update to 2.3.0rc8

* Thu Jul 22 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.10.rc7
- add Br qtsinglecoreapplication-devel
- add patch so nox uses qtsinglecoreapplication

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.9.rc7
- revert last commit

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.8.rc7
- disable qtsingleapplication for nox build

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.7.rc7
- update to 2.3.0rc7

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.6.rc6
- disable extra debugging

* Wed Jul 21 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.5.rc6
- update to 2.3.0rc6
- drop Br gtk3-devel
- add Br qtsingleapplication-devel
- use system qtsingleapplication

* Mon Jul 19 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.4.rc5
- update to 2.3.0rc5
- add patch to fix libnotify gtk problem

* Thu Jul 08 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.3.rc2
- update to 2.3.0rc2
- add Br gtk3-devel
- fix qt deprecated warning

* Sun Jun 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.2.beta2
- update to 2.3.0beta2

* Mon May 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.3.0-0.1.beta1
- update to 2.3.0beta1

* Mon May 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.8-1
- update to 2.2.8

* Thu May 13 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.7-1
- update to 2.2.7

* Sun Apr 18 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.6-1
- update to 2.2.6

* Wed Apr 07 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.5-1
- update to 2.2.5

* Tue Apr 06 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-1
- update to 2.2.4

* Sun Apr 04 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-1
- update to 2.2.3
- drop upstream patch (disable peer host name resolution)

* Fri Apr 02 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.2-2
- add patch to disable peer host name resolution (bz577723)

* Mon Mar 22 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.2-1
- update to 2.2.2
- remove upstream patches (abrt & robust_resume)

* Sun Mar 21 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-3
- add robust_resume patch

* Sat Mar 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-2
- add abrt patch

* Sat Mar 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.1-1
- update to 2.2.1

* Sun Mar 14 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Mon Mar 08 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.12.rc2
- update to 2.2.0rc2

* Thu Mar 04 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.11.rc1
- update to 2.2.0rc1

* Wed Feb 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.10.beta4
- rebuilt for new qt version

* Wed Feb 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.9.beta4
- rebuilt for new qt version

* Wed Feb 10 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.8.beta4
- update to 2.2.0beta4
- drop upstream patch
- add build require GeoIP-devel

* Tue Feb 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.7.beta3
- redo duplicate crash patch (svn 3564)

* Tue Feb 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.6.beta3
- add duplicate crash patch to fix crash when adding 
  a torrent that already exists in the transfer list
- add patch to fix DSO link problem

* Mon Feb 08 2010 leigh scott <leigh123linux@googlemail.com> - 2.2.0-0.5.beta3
- update to 2.2.0beta3

* Sun Jan 31 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.4.beta2
- update to 2.2.0beta2
- drop upstream patch

* Mon Jan 25 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.3.beta1
- add patch to Fix alternative upload speed limit overwriting

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.2.beta1
- add patch to disable extra debugging (corrects build flags)

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-0.1.beta1
- update to 2.2.0beta1

* Sun Jan 24 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.2-1
- update to 2.1.2
- drop gcc patch

* Thu Jan 21 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-3
- add some docs to the nox package

* Wed Jan 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-2
- seperate the gui and nox build processes so debuginfo is built properly

* Wed Jan 20 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.1-1
- update to 2.1.1

* Mon Jan 18 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.0-1
- update to 2.1.0

* Sun Jan 17 2010 leigh scott <leigh123linux@googlemail.com> - 2.1.0-0.13.rc7
- add patch to fix height of the status filters list

* Thu Jan 15 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.12.rc7
- add patch to use HTTP digest mode for Web UI authentication

* Thu Jan 14 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.11.rc7
- update to 2.1.0rc7

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.10.rc6
- update to 2.1.0rc6

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.9.rc5
- drop disable extra debug from gcc patch

* Mon Jan 11 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.8.rc5
- update to 2.1.0rc5
- drop nox patch

* Sat Jan 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.7.rc4
- disable geoip database and libnotify for the headless version
- add patch so nox doesn't require libQtGui.so.4
- correct previous date in changelog

* Sat Jan 09 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.6.rc4
- update to 2.1.0rc4
- build headless version as well

* Tue Jan 05 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.5.rc3
- update to 2.1.0rc3

* Sun Jan 03 2010 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.4.rc2
- update to 2.1.0rc2

* Wed Dec 30 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.3.beta3
- update to 2.1.0beta3

* Wed Dec 23 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.2.beta1
- update to 2.1.0beta2

* Sun Dec 20 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.1.0-0.1.beta1
- update to 2.1.0beta1
- disable extra debugging to gcc patch

* Fri Dec 18 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-1
- update to 2.0.2
- add gcc patch to fix #548491

* Mon Dec 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- update to 2.0.1
- clean up spec file

* Thu Dec 10 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-1
- update to 2.0.0

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.13.svn3058
- update to svn 3058 (RC6)

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.12.svn3054
- change requires qt4

* Mon Dec 07 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.11.svn3054
- update to svn 3054
- add Br: libnotify-devel

* Sun Dec 06 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.10.svn3043
- update to svn 3043

* Wed Dec 02 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.9.svn3027
- update to svn 3027

* Sun Nov 29 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.8.svn3011
- update to svn 3011

* Fri Nov 27 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.7.svn2985
- update to svn 2985

* Thu Nov 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.6.svn2979
- update to svn 2979

* Tue Nov 24 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.5.svn2930
- update to svn 2930

* Tue Nov 24 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.4.svn2927
- update to svn 2927

* Sun Nov 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-0.3.svn2885
- BR: qt4-devel, Requires: qt4 >= %%_qt4_version

* Sun Nov 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.2svn2885
- update to svn 2885

* Sun Nov 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-0.1svn2879
- update to svn 2879
- Drop Build requires  zziplib-devel and curl-devel

* Thu Nov 19 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.5.6-1
- update to 1.5.6

* Wed Nov 04 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.5-1
- update to 1.5.5

* Tue Oct 27 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.4-2
- rebuilt for qt 4.6

* Sun Oct 25 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.4-1
- update to 1.5.4
- drop flags patch

* Fri Oct 02 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.3-3
- bump spec due to cvs tagging error

* Fri Oct 02 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.3-2
- Rebuild for rb_libtorrent-0.14.6

* Thu Oct 01 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3

* Tue Sep 22 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2

* Thu Sep 10 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.1-2
- correct prep section package name

* Thu Sep 10 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.0-0.2.20090829svn
- add icons_qrc.patch

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.5.0-0.1.20090829svn
- update to svn 2578
- redo qbittorrent_flag patch (again :-( )

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-3
- redo qbittorrent_flag patch (again :-( )

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-2
- redo qbittorrent_flag patch

* Sat Aug 29 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.1-1
- update to 1.4.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.0-0.10.rc2
- rebuilt with new openssl

* Fri Aug 07 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.9.rc2
- correct prep section package name

* Fri Aug 07 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.8.rc2
- update to 1.4.0rc2

* Mon Aug 03 2009 leigh scott <leigh123linux@googlemail.com> - 1.4.0-0.7.20090803svn
- update to svn 2417

* Sat Jul 25 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.6.20090725svn
- update to svn 2409

* Wed Jul 15 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.5.20090715svn
- update to svn 2385

* Tue Jun 23 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.4.20090429svn
- replace update-mime-database with update-desktop-database
- update scriplets to the latest guidelines
- clean up white space

* Thu Jun 4 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.3.20090429svn
- Rebuild against the new rb_libtorrent version 0.14.4

* Fri May 22 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.2.20090429svn
- rebuild against boost-1.39

* Thu Apr 30 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-0.1.20090429svn
- Correct version & release tag
- Update to svn 2341 

* Wed Apr 29 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.4.2340svn
- Rebuild against the new rb_libtorrent version 0.14.3

* Sun Apr 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.3.2340svn
- Fix command to generate tarball

* Sun Apr 26 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.2.2340svn
- Fixes peference UI bug and splash screen  (launchpad 366957)

* Sat Apr 25 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-3.1.1511bzr
- Update to bzr 1511 

* Thu Apr 9 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-2
- Remember to update Source in spec file 

* Thu Apr 9 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.3-1
- update to version 1.3.3

* Sat Mar 7 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-13
- Had problems with cvs commit

* Sat Mar 7 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-12
- update to version 1.3.2

* Wed Mar 4 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-11
- Remove qhostaddress.h.patch 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-9
- add Br glib2-devel

* Mon Feb 23 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-8
- Add patch to fix qt build error (Thanks for the fix Rex)

* Mon Feb 9 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-7
- add patch to remove flags from menu to conform to Fedora 
- packaging guidelines.

* Sun Feb 8 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-6
- add more changes for review  

* Sat Feb 7 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.1-5
- update to 1.3.1 and add more recommended changes for review

* Thu Feb 5 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-4
- add update-mime-database to the post & postun sections

* Thu Feb 5 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-3
- add recommended changes for review

* Wed Jan 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-2
- clean up spec file

* Wed Jan 14 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-1
- update version

* Tue Jan 6 2009 Leigh Scott <leigh123linux@googlemail.com> - 1.3bzr1436
- bzr build 1436

* Fri Nov 7 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.3bzr1303
- first bzr build
- remove libMagick++ dependency 

* Tue Nov 4 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-2
- add requires qbittorrent-release

* Tue Nov 4 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-1
- update version

* Thu Oct 9 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-5
- rebuild against the rebuilt rb_libtorrent package

* Thu Oct 9 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-4
- build with gmake & fix group tag 

* Wed Oct 8 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-3
- rebuild to fix destop file + icon

* Wed Oct 8 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.1.4-2
- rebuild

* Sun Apr 13 2008 - Leigh Scott <leigh123linux@googlemail.com> 
- Initial release

