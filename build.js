const fs = require('fs');
const path = require('path');

// Configuration
const config = {
  sourceDir: '.',
  outputDir: '.',
  assetsDir: 'assets',
  cssDir: 'css',
  jsDir: 'js',
  templatesDir: 'templates'
};

// Create directories if they don't exist
function ensureDirectories() {
  const dirs = [config.assetsDir, config.cssDir, config.jsDir, config.templatesDir];
  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// Move assets
function moveAssets() {
  const assets = ['julien.jpg'];
  assets.forEach(asset => {
    const sourcePath = path.join(config.sourceDir, asset);
    const destPath = path.join(config.assetsDir, asset);
    if (fs.existsSync(sourcePath)) {
      fs.copyFileSync(sourcePath, destPath);
      console.log(`Moved ${asset} to assets/`);
    }
  });
}

// Generate HTML files from templates
function generateHTMLFiles() {
  const pages = [
    {
      name: 'index.html',
      title: 'Home',
      description: 'Julien Simon - Chief Evangelist @ Arcee AI',
      template: 'templates/index.html'
    },
    {
      name: 'experience.html',
      title: 'Experience',
      description: 'Professional experience and career highlights of Julien Simon',
      template: 'templates/experience.html'
    },
    {
      name: 'speaking.html',
      title: 'Speaking',
      description: 'Speaking engagements and presentations by Julien Simon',
      template: 'templates/speaking.html'
    },
    {
      name: 'media.html',
      title: 'Media',
      description: 'Media appearances and interviews featuring Julien Simon',
      template: 'templates/media.html'
    },
    {
      name: 'publications.html',
      title: 'Publications',
      description: 'Publications and blog posts by Julien Simon',
      template: 'templates/publications.html'
    },
    {
      name: 'code.html',
      title: 'Code',
      description: 'Code samples and projects by Julien Simon',
      template: 'templates/code.html'
    },
    {
      name: 'youtube.html',
      title: 'YouTube',
      description: 'YouTube videos and content by Julien Simon',
      template: 'templates/youtube.html'
    },
    {
      name: 'books.html',
      title: 'Books',
      description: 'Books and publications by Julien Simon',
      template: 'templates/books.html'
    }
  ];

  pages.forEach(page => {
    if (fs.existsSync(page.template)) {
      let content = fs.readFileSync(page.template, 'utf8');
      content = content.replace('{{PAGE_TITLE}}', page.title);
      content = content.replace('{{PAGE_DESCRIPTION}}', page.description);
      
      fs.writeFileSync(page.name, content);
      console.log(`Generated ${page.name}`);
    }
  });
}

// Create package.json for project management
function createPackageJson() {
  const packageJson = {
    "name": "julien-simon-website",
    "version": "1.0.0",
    "description": "Personal website of Julien Simon - Chief Evangelist @ Arcee AI",
    "main": "index.html",
    "scripts": {
      "build": "node build.js",
      "serve": "python3 -m http.server 8000",
      "dev": "python3 -m http.server 8000"
    },
    "keywords": ["personal-website", "ai", "machine-learning", "cloud-computing"],
    "author": "Julien Simon",
    "license": "MIT",
    "devDependencies": {},
    "dependencies": {}
  };

  fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
  console.log('Created package.json');
}

// Create README
function createREADME() {
  const readme = `# Julien Simon - Personal Website

Professional website of Julien Simon, Chief Evangelist at Arcee AI.

## Features

- 🎨 Modern, responsive design

- 📱 Mobile-first approach
- ⚡ Fast loading with optimized assets
- 🔍 SEO optimized
- 📊 Analytics integration

## Structure

\`\`\`
juliensimon.github.io/
├── assets/          # Images and static assets
├── css/            # Stylesheets
├── js/             # JavaScript files
├── templates/      # HTML templates
├── index.html      # Home page
├── experience.html # Experience page
├── speaking.html   # Speaking engagements
├── media.html      # Media appearances
├── publications.html # Publications
├── code.html       # Code samples
├── youtube.html    # YouTube content
├── books.html      # Books and publications
└── README.md       # This file
\`\`\`

## Development

1. Clone the repository
2. Run \`npm install\` (optional)
3. Run \`npm run dev\` to start local server
4. Open http://localhost:8000

## Build

Run \`npm run build\` to regenerate HTML files from templates.

## Technologies

- HTML5
- CSS3 with CSS Custom Properties
- Vanilla JavaScript
- Font Awesome Icons
- Inter Font Family

## License

MIT License
`;

  fs.writeFileSync('README.md', readme);
  console.log('Created README.md');
}

// Main build function
function build() {
  console.log('🚀 Starting build process...');
  
  ensureDirectories();
  moveAssets();
  generateHTMLFiles();
  createPackageJson();
  createREADME();
  
  console.log('✅ Build completed successfully!');
  console.log('\n📁 Project structure:');
  console.log('├── assets/     (images and static files)');
  console.log('├── css/        (stylesheets)');
  console.log('├── js/         (JavaScript files)');
  console.log('├── templates/  (HTML templates)');
  console.log('└── *.html      (generated pages)');
  console.log('\n🌐 To view the site: npm run dev');
}

// Run build if this file is executed directly
if (require.main === module) {
  build();
}

module.exports = { build }; 