%global gem_name rspec-core
%global	majorver	3.5.3
#%%global	preminorver	.rc6
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	fedorarel	2

%global	gem_name	rspec-core


# %%check section needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core
%global	need_bootstrap_set	1

%{!?need_bootstrap:	%global	need_bootstrap	%{need_bootstrap_set}}

Summary:	Rspec-3 runner and formatters
Name:		rubygem-%{gem_name}
Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}.0

Group:		Development/Languages
License:	MIT
URL:		https://github.com/rspec/rspec-core
Source0:	https://rubygems.org/gems/%{gem_name}-%{fullver}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
%if 0%{?need_bootstrap} < 1
BuildRequires:	rubygem(ZenTest)
BuildRequires:	rubygem(nokogiri)
BuildRequires:	rubygem(rake)
BuildRequires:	rubygem(rspec-expectations)
BuildRequires:	rubygem(rspec-mocks)
BuildRequires:	rubygem(aruba)
%endif
Requires:	rubygem(rspec-support) >= 3.5.0
Requires:	rubygem(rspec-support) < 3.6
Requires:	ruby(release)
# When killing the below dependency, a notification to mailing list
# is needed
#Requires:	rubygem(rspec-expectations)
#Requires:	rubygem(rspec-mocks)
# Make the following installed by default
# lib/rspec/core/rake_task
Requires:	rubygem(rake)
# Optional
#Requires:	rubygem(ZenTest)
#Requires:	rubygem(mocha)
#Requires:	rubygem(ruby-debug)
# Not found in Fedora yet (and optional)
#Requires:	rubygem(rr)
Provides:	rubygem(%{gem_name}) = %{version}-%{release}
BuildArch:	noarch

%description
Behaviour Driven Development for Ruby.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/exe -type f | xargs chmod a+x

%if 0%{?need_bootstrap} < 1
%check
LANG=en_US.UTF-8
pushd .%{gem_instdir}
# Test failure needs investigation...
# There are is some missing template for Ruby 2.0.0:
# https://github.com/rspec/rspec-core/commits/master/spec/rspec/core/formatters/html_formatted-2.0.0.html
ruby -rubygems -Ilib/ -S exe/rspec || :
%endif

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE.md
%{_bindir}/rspec
%{gem_instdir}/exe/
%{gem_instdir}/lib/

%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%defattr(-,root,root,-)
%{gem_docdir}
%doc %{gem_instdir}/.document
%doc %{gem_instdir}/Changelog.md
%doc %{gem_instdir}/README.md

%changelog
* Tue Sep 20 2016 Rich Megginson <rmeggins@redhat.com> - 3.5.3-2
- fix bin path - must be /exe for other rspec tools

* Fri Aug 26 2016 Rich Megginson <rmeggins@redhat.com> - 3.5.3-1
- update to 3.5.3

* Fri Aug 01 2014 Troy Dawson <tdawson@redhat.com> - 2.14.8-1.0
- Remove testing to break dependency circle

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.8-1
- 2.14.8

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.7-1
- 2.14.7

* Thu Oct 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.6-1
- 2.14.6

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.14.5-1
- 2.14.5

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- Again enable test suite

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-3
- Bootstrap for rubygem-gherkin <- rubygem-cucumber

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.1-1
- 2.13.1

* Tue Feb 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-2
- Use aruba, which is already in Fedora, drop no-longer-needed
  patch

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.2-1
- 2.12.2

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.11.1-1
- 2.11.1
- Drop dependency for mocks and expectations

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 21 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.8.0-1
- 2.8.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.4-1
- 2.6.4

* Wed May 25 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.3-1
- 2.6.3

* Tue May 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.2-2
- Workaround for invalid date format in gemspec file (bug 706914)

* Mon May 23 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.2-1
- 2.6.2

* Mon May 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-1
- 2.6.0

* Tue May 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.2.rc6
- 2.6.0 rc6

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.6.0-0.1.rc4
- 2.6.0 rc4

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- And enable check on rawhide

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-3
- More cleanups

* Tue Feb 22 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-2
- Some misc fixes

* Thu Feb 17 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.1-1
- 2.5.1

* Fri Nov 05 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- Initial package
