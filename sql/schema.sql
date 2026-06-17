USE GitActivityDB;
GO

IF OBJECT_ID('dbo.Commits', 'U') IS NOT NULL
    DROP TABLE dbo.Commits;
GO

IF OBJECT_ID('dbo.Repositories', 'U') IS NOT NULL
    DROP TABLE dbo.Repositories;
GO

CREATE TABLE dbo.Repositories
(
    RepositoryID INT IDENTITY(1,1) PRIMARY KEY,

    Username NVARCHAR(100) NOT NULL,

    RepositoryName NVARCHAR(255) NOT NULL,

    RepositoryPath NVARCHAR(500) NOT NULL,

    ScanDate DATETIME DEFAULT GETDATE()
);
GO



CREATE TABLE dbo.Commits
(
    CommitID INT IDENTITY(1,1) PRIMARY KEY,

    RepositoryID INT NOT NULL,

    CommitHash NVARCHAR(100) NOT NULL,

    CommitMessage NVARCHAR(MAX) NOT NULL,

    CommitCategory NVARCHAR(50) NULL,

    AuthorName NVARCHAR(255) NOT NULL,

    CommitDate DATETIME NOT NULL,

    FOREIGN KEY (RepositoryID)
        REFERENCES dbo.Repositories(RepositoryID)
        ON DELETE CASCADE
);
GO



CREATE INDEX IX_Repositories_Username
ON dbo.Repositories(Username);
GO

CREATE INDEX IX_Commits_RepositoryID
ON dbo.Commits(RepositoryID);
GO

CREATE INDEX IX_Commits_CommitDate
ON dbo.Commits(CommitDate);
GO