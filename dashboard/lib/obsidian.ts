interface ObsidianNote {
  title: string
  content: string
  tags?: string[]
  folder?: string
}

interface ObsidianConfig {
  vaultPath: string
  apiPort?: number
  apiKey?: string
}

export class ObsidianIntegration {
  private config: ObsidianConfig
  private baseUrl: string

  constructor(config: ObsidianConfig) {
    this.config = config
    this.baseUrl = `http://localhost:${config.apiPort || 27124}`
  }

  private async makeRequest(endpoint: string, method: string = 'GET', body?: any) {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }

    if (this.config.apiKey) {
      headers['Authorization'] = `Bearer ${this.config.apiKey}`
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Obsidian API request failed:', error)
      throw error
    }
  }

  async createNote(note: ObsidianNote) {
    const path = note.folder 
      ? `${this.config.vaultPath}/${note.folder}/${note.title}.md`
      : `${this.config.vaultPath}/${note.title}.md`

    const frontmatter = note.tags && note.tags.length > 0
      ? `---\ntags: [${note.tags.join(', ')}]\ncreated: ${new Date().toISOString()}\n---\n\n`
      : ''

    const content = frontmatter + note.content

    return await this.makeRequest('/vault/create', 'POST', {
      path,
      content,
    })
  }

  async updateNote(path: string, content: string) {
    return await this.makeRequest('/vault/update', 'PUT', {
      path: `${this.config.vaultPath}/${path}`,
      content,
    })
  }

  async searchNotes(query: string) {
    return await this.makeRequest(`/search?query=${encodeURIComponent(query)}`)
  }

  async getNote(path: string) {
    return await this.makeRequest(`/vault/${encodeURIComponent(path)}`)
  }

  async listNotes(folder?: string) {
    const path = folder ? `${this.config.vaultPath}/${folder}` : this.config.vaultPath
    return await this.makeRequest(`/vault/list?path=${encodeURIComponent(path)}`)
  }

  async createDailyNote(content: string) {
    const today = new Date().toISOString().split('T')[0]
    return await this.createNote({
      title: today,
      content,
      folder: 'Daily Notes',
      tags: ['daily-note']
    })
  }

  async appendToNote(path: string, content: string) {
    const existingNote = await this.getNote(path)
    const newContent = existingNote.content + '\n\n' + content
    return await this.updateNote(path, newContent)
  }
}

// React hook for Obsidian integration
import { useState, useCallback } from 'react'

export function useObsidian(config: ObsidianConfig) {
  const [obsidian] = useState(() => new ObsidianIntegration(config))
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const executeAction = useCallback(async <T,>(
    action: () => Promise<T>
  ): Promise<T | null> => {
    setIsLoading(true)
    setError(null)
    
    try {
      const result = await action()
      return result
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      return null
    } finally {
      setIsLoading(false)
    }
  }, [])

  const createNote = useCallback(
    (note: ObsidianNote) => executeAction(() => obsidian.createNote(note)),
    [obsidian, executeAction]
  )

  const updateNote = useCallback(
    (path: string, content: string) => executeAction(() => obsidian.updateNote(path, content)),
    [obsidian, executeAction]
  )

  const searchNotes = useCallback(
    (query: string) => executeAction(() => obsidian.searchNotes(query)),
    [obsidian, executeAction]
  )

  const getNote = useCallback(
    (path: string) => executeAction(() => obsidian.getNote(path)),
    [obsidian, executeAction]
  )

  const listNotes = useCallback(
    (folder?: string) => executeAction(() => obsidian.listNotes(folder)),
    [obsidian, executeAction]
  )

  const createDailyNote = useCallback(
    (content: string) => executeAction(() => obsidian.createDailyNote(content)),
    [obsidian, executeAction]
  )

  const appendToNote = useCallback(
    (path: string, content: string) => executeAction(() => obsidian.appendToNote(path, content)),
    [obsidian, executeAction]
  )

  return {
    createNote,
    updateNote,
    searchNotes,
    getNote,
    listNotes,
    createDailyNote,
    appendToNote,
    isLoading,
    error
  }
}