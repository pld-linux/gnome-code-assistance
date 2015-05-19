#
# Conditional build:
%bcond_without	llvm	# (LLVM based) C backend
%bcond_without	golang	# Go backend
#
%ifarch x32 ppc64
%undefine	with_llvm
%endif
%ifnarch %{ix86} %{x8664} %{arm}
%undefine	with_golang
%endif
Summary:	Common code assistance services for code editors
Summary(pl.UTF-8):	Wspólne usługi wspierające pracę z kodem dla edytorów kodu
Name:		gnome-code-assistance
Version:	3.16.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-code-assistance/3.16/%{name}-%{version}.tar.xz
# Source0-md5:	356a034dd60271f39f3d5ce658b75f09
URL:		https://wiki.gnome.org/Projects/CodeAssistance
BuildRequires:	gjs-devel
BuildRequires:	glib2 >= 1:2.36
BuildRequires:	gobject-introspection
# version with just "go" executable
BuildRequires:	golang >= 1.3
BuildRequires:	llvm-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-dbus
BuildRequires:	python3-pygobject3 >= 3.8
BuildRequires:	python3-simplejson
# with ripper module
BuildRequires:	ruby >= 1:1.9.1
BuildRequires:	ruby-dbus
BuildRequires:	ruby-sass >= 3.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.20
BuildRequires:	vala-libgee >= 0.8
BuildRequires:	xz
Requires:	glib2 >= 1:2.36
Requires:	gobject-introspection
Requires:	libgee >= 0.8
Requires:	python3 >= 1:3.2
Requires:	python3-dbus
Requires:	python3-pygobject3 >= 3.8
Requires:	python3-simplejson
Requires:	ruby >= 1:1.9.1
Requires:	ruby-dbus
Requires:	ruby-sass >= 3.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gnome-code-assistance is a project which aims to provide common code
assistance services for code editors (simple editors as well as IDEs).
It is an effort to provide a centralized code-assistance as a service
for the GNOME platform instead of having every editor implement their
own solution.

%description -l pl.UTF-8
gnome-code-assistance to projekt mający na celu dostarczenie wspólnych
usług wspierających pracę z kodem dla edytorów kodu (zarówno prostych
edytorów, jak i IDE). Jest to próba zapewnienia centralnego wsparcia
edycji kodu jako usługi dla platformy GNOME zamiast implementowania
własnego rozwiązania w każdym edytorze.

%prep
%setup -q

%build
%configure \
	%{!?with_llvm:--disable-c} \
	%{!?with_golang:--disable-go} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -i -e '1s,/usr/bin/env gjs,/usr/bin/gjs,' $RPM_BUILD_ROOT%{_libexecdir}/gnome-code-assistance/js
%{__sed} -i -e '1s,/usr/bin/env python3,/usr/bin/python3,' $RPM_BUILD_ROOT%{_libexecdir}/gnome-code-assistance/{c,json,python,sh,xml}
%{__sed} -i -e '1s,/usr/bin/env ruby,/usr/bin/ruby,' $RPM_BUILD_ROOT%{_libexecdir}/gnome-code-assistance/{css,ruby}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libexecdir}/gnome-code-assistance
%if %{with llvm}
# R: python3, llvm
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/c
%endif
# R: ruby, ruby-sass
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/css
%if %{with golang}
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/go
%endif
# R: gjs
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/js
# R: python3, python3-simplejson
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/json
# R: python3
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/python
# R: ruby
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/ruby
# R: python3
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/sh
# R: glib2 libgee
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/vala
# R: vala (libvala)
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/valahelper
# R: python3
%attr(755,root,root) %{_libexecdir}/gnome-code-assistance/xml
%dir %{_libexecdir}/gnome-code-assistance/backends
%{_libexecdir}/gnome-code-assistance/backends/js
# R: python3-dbus
%{_libexecdir}/gnome-code-assistance/backends/py
# R: ruby-dbus
%{_libexecdir}/gnome-code-assistance/backends/rb
%{_datadir}/dbus-1/services/org.gnome.CodeAssist.v1.*.service
%{_datadir}/glib-2.0/schemas/org.gnome.codeassistance.gschema.xml
