# HTTP Listing  resource

Tracks the versions available for resources available via an HTTP
directory listing, such as those available in Apache or NGINX web
servers.

Directories must be structured with a directory for each version,
with the binary and, optionally, source contents within that
directory. The naming convention of the directories can be customized,
provided that semantic versioning is used.

For example, the Hadoop directory listing could be configured as follows:

```yaml
resources:
- name: hadoop
  type: http-listing
  source:
    url: http://www-us.apache.org/dist/hadoop/core
    prefix: hadoop-
    hash-format: mds
    hash-algorithm: sha1
    binary-suffix: .tar.gz
    source-suffix: -src.tar.gz
    mds-suffix: .tar.gz.mds
```

Which would result in the following configuration:

```
  + Root URL
  |
  +-- <prefix><version>
      |
      +-- <prefix><version><binary-suffix>
      |
      +-- <prefix><version><source-suffix>
      |
      +-- <prefix><version><mds-suffix>
      |
```

And support the following directory

```
  + Root URL
  |
  +-- hadoop-1.2.1
      |
      +-- hadoop-1.2.1.tar.gz
      |
      +-- hadoop-1.2.1.tar.gz.mds
      |
      +-- hadoop-1.2.1-src.tar.gz
      |
  +-- hadoop-2.6.1
      |
      +-- hadoop-2.6.1.tar.gz
      |
      +-- hadoop-2.6.1.tar.gz.mds
      |
      +-- hadoop-2.6.1-src.tar.gz
      |
  ...
  ...
```

The Initial directories in the listing must be compatible with semantic
versioning to be recognized.

For example, to automatically consume releases of
[Hadoop](https://www.apache.org/hadoop):

## Source Configuration

* `url`: *Required.* The base URL from which there are available version directories.
* `prefix`: A prefix applied to all directory contents -- versions & binaries
* `suffix`: A suffix applied to all directory contents -- versions & binaries
* `version-prefix`: A prefix applied to version directory contents
* `binary-prefix`: A prefix applied to binary directory contents
* `source-prefix`: A prefix applied to source directory contents
* `version-suffix`: A suffix applied to version directory contents
* `binary-suffix`: A suffix applied to binary directory contents
* `source-suffix`: A suffix applied to source directory contents
* `hash-format`: Type of file format containing binary file digest hash. Valid options are mds, md5,
and sha1.
* `hash-algorithm`: Hashing algorithm used to check binary file validity. Valid options are sha1, sha384, sha256, sha512, md5
* `hash-prefix`: A prefix applied to hash verification file
* `hash-suffix`: A suffix applied to hash verification file

## Behavior

### `check`: Check for new versions of the release.

Detects new versions of the release that have been published to the URL, according to
semantic versioning. If no version is specified, `check` returns all versions in order;
otherwise, `check` returns all versions from the version specified on.

### `in`: Fetch a version of the release.

Fetches a given release, placing the following in the destination:

*  The binary or archive contents of the binary content, if it is a valid archive.
* `version`: The version number of the release.
* `url`: A URL that can be used to download directory contents
* A hash digest file. The actual file name will match the hashing algorithm used.
* The source tarball, if the `tarball` param is `true`. Actual file name will match the downloaded file.

#### Parameters

* `tarball`: *Optional.* Default `false`. Fetch the release tarball.
