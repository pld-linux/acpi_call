# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools

%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%define		rel	1
%define		pname	acpi_call
Summary:	A linux kernel module that enables calls to ACPI methods through /proc/acpi/call
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	1.1.0
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	GPL v2
Group:		Base/Kernel
Source0:	https://github.com/mkottman/acpi_call/archive/v%{version}/%{pname}-%{version}.tar.gz
# Source0-md5:	f69d40e130b0e5ed17ce8adb19e6dda1
Patch0:		%{pname}-build.patch
URL:		https://github.com/mkottman/acpi_call
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}}
BuildRequires:	rpmbuild(macros) >= 1.701
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A linux kernel module that enables calls to ACPI methods through
/proc/acpi/call.

%package -n %{pname}-scripts
Summary:	This package contains sample scripts for acpi_call kernel module
Group:		Applications/System
BuildArch:	noarch

%description -n %{pname}-scripts
This package contains sample scripts for acpi_call kernel module.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-misc-acpi_call\
Summary:	A linux kernel module that enables calls to ACPI methods through /proc/acpi/call\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-misc-acpi_call\
A linux kernel module that enables calls to ACPI methods through\
/proc/acpi/call.\
%files -n kernel%{_alt_kernel}-misc-acpi_call\
%defattr(644,root,root,755)\
%doc README.md\
/lib/modules/%{_kernel_ver}/misc/acpi_call.ko*\
\
%post	-n kernel%{_alt_kernel}-misc-acpi_call\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-misc-acpi_call\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m acpi_call\
%install_kernel_modules -D installed -m acpi_call -d misc\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%build
%{?with_kernel:%{expand:%build_kernel_packages}}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_datadir}/acpi_call
cp -a examples/* $RPM_BUILD_ROOT%{_datadir}/acpi_call
%endif

%if %{with kernel}
cp -a installed/* $RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%files -n %{pname}-scripts
%defattr(644,root,root,755)
%dir %{_datadir}/acpi_call
%attr(755,root,root) %{_datadir}/acpi_call/*.sh
%endif
