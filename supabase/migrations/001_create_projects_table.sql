CREATE TYPE project_status AS ENUM ('planning', 'in_progress', 'completed');
CREATE TYPE project_priority AS ENUM ('low', 'medium', 'high');

CREATE TABLE projects (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                  UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title                    TEXT NOT NULL,
    description              TEXT,
    status                   project_status NOT NULL DEFAULT 'planning',
    priority                 project_priority NOT NULL DEFAULT 'medium',
    estimated_duration_hours NUMERIC,
    estimated_cost           NUMERIC,
    instructions             JSONB NOT NULL DEFAULT '[]'::jsonb,
    materials                JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own projects"
    ON projects FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own projects"
    ON projects FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own projects"
    ON projects FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete their own projects"
    ON projects FOR DELETE USING (auth.uid() = user_id);
